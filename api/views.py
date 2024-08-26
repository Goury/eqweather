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
    There are all the cells in the database.
    Each contains cell coordinates and a link to query every weather forecast for the given cell.
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
    API endpoint to view weather forecasts for a given cell.
    Each forecast also contains a link to query all the cell forecasts for the same timestamp.
    """
    queryset = WeatherForecast.objects.all()
    serializer_class = WeatherForecastSerializer
    permission_classes = []

    def get_queryset(self):
        return WeatherForecast.objects.filter(cell_id=self.kwargs['id'])


class ForecastPerTimeList(generics.ListAPIView):
    """
    API endpoint to view weather forecasts for a given period of time.
    Each forecast also contains a link to query forecasts for all the timestamps from the same cell.
    """
    queryset = WeatherForecast.objects.all()
    serializer_class = WeatherForecastPerTimeSerializer
    permission_classes = []

    def get_queryset(self):
        return WeatherForecast.objects.filter(when__when=self.kwargs['datetime'])


class TimesList(generics.ListAPIView):
    """
    API endpoint to view available weather forecast timestamps.
    These are all the timestamps for which there is any data.
    Each contains readable date and time and a link to query all the data points for the given time.
    """
    queryset = ForecastDateTime.objects.all()
    serializer_class = ForecastDateTimeSerializer
    permission_classes = []
