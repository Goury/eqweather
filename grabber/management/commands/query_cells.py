from django.conf import settings
from django.core.management.base import BaseCommand

from grabber.models import GridCell

from decimal import Decimal
import json
import numpy
import requests

headers = requests.utils.default_headers()
headers['User-Agent'] = settings.USER_AGENT
headers['Accept'] = 'application/geo+json'


class Command(BaseCommand):
    help = 'Query weather API for cells'

    def add_arguments(self, parser):
        parser.add_argument('--silent',
            action='store_true',
            dest='silent',
            default=False,
            help='Do not print anything')
        parser.add_argument('--lat-start',
            dest='lat-start',
            default='',
            help='Starting latitude')
        parser.add_argument('--lon-start',
            dest='lon-start',
            default='',
            help='Starting longitude')
        parser.add_argument('--lat-end',
            dest='lat-end',
            default='',
            help='Ending latitude')
        parser.add_argument('--lon-end',
            dest='lon-end',
            default='',
            help='Ending longitude')
        parser.add_argument('--steps',
            dest='steps',
            default='20',
            help='Number of steps to go in each direction')

    def query_cell(self, lat, lon):
        url = f'{settings.API_ENDPOINT}/points/{lat},{lon}'
        response = requests.get( url, headers=headers )
        data = json.loads(response.content.decode())
        GridCell.objects.get_or_create(
            grid_id=data['properties']['gridId'],
            grid_x=data['properties']['gridX'],
            grid_y=data['properties']['gridY'],
        )

    def handle(self, *args, **kwargs):
        lat_1 = Decimal(kwargs['lat-start'])
        lon_1 = Decimal(kwargs['lon-start'])
        lat_2 = Decimal(kwargs['lat-end'])
        lon_2 = Decimal(kwargs['lon-end'])
        steps = int(kwargs['steps'])
        lat_range = numpy.linspace(lat_1, lat_2, steps)
        lon_range = numpy.linspace(lon_1, lon_2, steps)
        for x in lat_range:
            for y in lon_range:
                if not kwargs['silent']: self.stdout.write(f'querying cell at [{x}] [{y}]')
                self.query_cell(x, y)
