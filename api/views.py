from grabber.models import GridCell, WeatherForecast, ForecastDateTime
from grabber.serializers import GridCellSerializer, WeatherForecastSerializer, WeatherForecastPerTimeSerializer, ForecastDateTimeSerializer

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'cells': reverse('api:cells', request=request, format=format),
        'times': reverse('api:times', request=request, format=format),
    })

class GridCellList(generics.ListAPIView):
    """
    API endpoint to view grid cells.
    """
    queryset = GridCell.objects.all().order_by('grid_id', 'grid_x', 'grid_y')
    serializer_class = GridCellSerializer
    permission_classes = []


class GridCellSingle(generics.RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = GridCellSerializer
    permission_classes = []

    def get_queryset(self):
        return GridCell.objects.filter(id=self.kwargs['id'])


class ForecastList(generics.ListAPIView):
    """
    API endpoint to view weather forecasts.
    """
    queryset = WeatherForecast.objects.all()
    serializer_class = WeatherForecastSerializer
    permission_classes = []

    def get_queryset(self):
        return WeatherForecast.objects.filter(cell_id=self.kwargs['id'])


class ForecastPerTimeList(generics.ListAPIView):
    """
    API endpoint to view weather forecasts for a given period of time.
    """
    queryset = WeatherForecast.objects.all()
    serializer_class = WeatherForecastPerTimeSerializer
    permission_classes = []

    def get_queryset(self):
        return WeatherForecast.objects.filter(when__when=self.kwargs['datetime'])


class TimesList(generics.ListAPIView):
    """
    API endpoint to view available weather forecast timestamps.
    """
    queryset = ForecastDateTime.objects.all()
    serializer_class = ForecastDateTimeSerializer
    permission_classes = []
