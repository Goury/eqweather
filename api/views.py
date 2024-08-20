from grabber.models import GridCell, WeatherForecast
from grabber.serializers import GridCellSerializer, WeatherForecastSerializer

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'cells': reverse('cells', request=request, format=format),
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
