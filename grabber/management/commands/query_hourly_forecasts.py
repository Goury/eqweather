from django.conf import settings
from django.core.management.base import BaseCommand

from grabber.models import GridCell, WeatherForecast

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

    def handle(self, *args, **kwargs):
        weather_forecasts = []
        for cell in GridCell.objects.all():
            if not kwargs['silent']: self.stdout.write(f'querying forecasts at [{cell.grid_id} {cell.grid_x},{cell.grid_y}]')
            url = f'{settings.API_ENDPOINT}/gridpoints/{cell.grid_id}/{cell.grid_x},{cell.grid_y}/forecast/hourly?units=si'
            response = requests.get(url, headers=headers)
            if response.status_code in [404, 500]:
                if not kwargs['silent']: self.stdout.write(f'Got status code {response.status_code} T_T')
                continue
            data = json.loads(response.content.decode())
            if data['geometry']['type'] == 'Polygon':
                cell.polygon_json = json.dumps(data['geometry']['coordinates'][0])
                cell.save()
            for period in data['properties']['periods']:
                weather_forecasts.append(
                    WeatherForecast(
                        cell=cell,
                        when=datetime.strptime(period['startTime'], '%Y-%m-%dT%H:%M:%S%z'),
                        temperature=period['temperature'],
                        humidity=period['relativeHumidity']['value'],
                    )
                )
        WeatherForecast.objects.bulk_create(weather_forecasts, 100, ignore_conflicts=True)
