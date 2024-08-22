from django.conf import settings
from django.core.management.base import BaseCommand

from grabber.models import ForecastDateTime, GridCell, WeatherForecast

from datetime import datetime
import json
import requests

headers = requests.utils.default_headers()
headers['User-Agent'] = settings.USER_AGENT
headers['Accept'] = 'application/geo+json'


class Command(BaseCommand):
    help = 'Query weather API for an hourly forecast for each cell'

    def add_arguments(self, parser):
        parser.add_argument('--silent',
            action='store_true',
            dest='silent',
            default=False,
            help='Do not print anything')

        parser.add_argument('--notravel',
            action='store_true',
            dest='notravel',
            default=False,
            help='Do not count temperature travel')


    def load_cells(self, q, silent, notravel):
        weather_forecasts = []
        unprocessed_cells = []
        for cell in q:
            if not silent: self.stdout.write(f'querying forecasts at [{cell.grid_id} {cell.grid_x},{cell.grid_y}]')
            url = f'{settings.API_ENDPOINT}/gridpoints/{cell.grid_id}/{cell.grid_x},{cell.grid_y}/forecast/hourly?units=si'
            response = requests.get(url, headers=headers)
            if response.status_code in [404, 500]:
                if response.status_code == 500:
                    unprocessed_cells.append(cell.id)
                if not silent: self.stdout.write(f'Got status code {response.status_code} T_T')
                continue
            data = json.loads(response.content.decode())
            if data['geometry']['type'] == 'Polygon':
                # Because in the United States latitude and longitude are coming out backwards even when queried forwards?
                processed_data = [[i[1], i[0]] for i in data['geometry']['coordinates'][0]]
                cell.polygon_json = json.dumps(processed_data)
                cell.save()
            for period in data['properties']['periods']:
                weather_forecasts.append(
                    WeatherForecast(
                        cell=cell,
                        when=ForecastDateTime.objects.get_or_create(when=datetime.strptime(period['startTime'], '%Y-%m-%dT%H:%M:%S%z'))[0],
                        temperature=period['temperature'],
                        humidity=period['relativeHumidity']['value'],
                    )
                )
            if not notravel:
                # Implement a basic data processing step such as basic statistics or aggregation by parameter
                temperatures = [ period['temperature'] for period in data['properties']['periods'] ]
                temperature_travel = [ max(temperatures[i], temperatures[i+1]) - min(temperatures[i], temperatures[i+1]) for i in range(len(temperatures)-1) ]
                if not silent: self.stdout.write(f'Temperature will travel for total of {sum(temperature_travel)} degrees in this cell')
        return weather_forecasts, unprocessed_cells

    def handle(self, *args, **kwargs):
        weather_forecasts, unprocessed_cells = self.load_cells(GridCell.objects.all(), kwargs['silent'], kwargs['notravel'])
        WeatherForecast.objects.bulk_create(weather_forecasts, 100, ignore_conflicts=True)
        while unprocessed_cells:
            if not kwargs['silent']: self.stdout.write(f'Attempting to query bad cells again')
            weather_forecasts, unprocessed_cells = self.load_cells(GridCell.objects.filter(id__in=unprocessed_cells), kwargs['silent'], kwargs['notravel'])
            WeatherForecast.objects.bulk_create(weather_forecasts, 100, ignore_conflicts=True)
