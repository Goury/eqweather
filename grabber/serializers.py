from django.conf import settings

from .models import GridCell, WeatherForecast, ForecastDateTime

from datetime import datetime
from rest_framework import serializers
from rest_framework.reverse import reverse


class GridCellSerializer(serializers.HyperlinkedModelSerializer):

    def get_forecasts(self, obj):
        uri = reverse('api:forecasts', args=[obj.id])
        return f'{settings.API_URL}{uri}'

    forecasts = serializers.SerializerMethodField('get_forecasts')

    class Meta:
        model = GridCell
        fields = ['id', 'grid_id', 'grid_x', 'grid_y', 'polygon_json', 'forecasts']


class WeatherForecastSerializer(serializers.HyperlinkedModelSerializer):

    def get_forecastdatetime(self, obj):
        uri = reverse('api:forecasts-per-time', args=[obj.when.when])
        return f'{settings.API_URL}{uri}'

    forecast_datetime = serializers.SerializerMethodField('get_forecastdatetime')

    class Meta:
        model = WeatherForecast
        fields = ['forecast_datetime', 'temperature', 'humidity']


class WeatherForecastPerTimeSerializer(serializers.HyperlinkedModelSerializer):

    def get_cell(self, obj):
        uri = reverse('api:cell', args=[obj.cell.id])
        return f'{settings.API_URL}{uri}'

    def get_cell_id(self, obj):
        return obj.cell.id

    cell = serializers.SerializerMethodField('get_cell')
    cell_id = serializers.SerializerMethodField('get_cell_id')

    class Meta:
        model = WeatherForecast
        fields = ['cell', 'cell_id', 'temperature', 'humidity']


class ForecastDateTimeSerializer(serializers.HyperlinkedModelSerializer):

    def get_when(self, obj):
        uri = reverse('api:forecasts-per-time', args=[obj.when])
        return f'{settings.API_URL}{uri}'

    def get_human_readable_when(self, obj):
        return datetime.strftime(obj.when, '%Y-%m-%d %H:%M')

    when = serializers.SerializerMethodField('get_when')
    human_readable_when = serializers.SerializerMethodField('get_human_readable_when')

    class Meta:
        model = ForecastDateTime
        fields = ['when', 'human_readable_when']
