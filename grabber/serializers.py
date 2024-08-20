from django.conf import settings

from .models import GridCell, WeatherForecast

from rest_framework import serializers
from rest_framework.reverse import reverse


class GridCellSerializer(serializers.HyperlinkedModelSerializer):

    def get_forecasts(self, obj):
        uri = reverse('forecasts', args=[obj.id])
        return f'{settings.API_URL}{uri}'

    forecasts = serializers.SerializerMethodField('get_forecasts')

    class Meta:
        model = GridCell
        fields = ['grid_id', 'grid_x', 'grid_y', 'polygon_json', 'forecasts']


class WeatherForecastSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WeatherForecast
        fields = ['when', 'temperature', 'humidity']
