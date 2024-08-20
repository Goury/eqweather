from django.urls import path

from . import views

urlpatterns = [
    path('', views.api_root),
    path('grid_cell/',                 views.GridCellList.as_view(),    name='cells'),
    path('grid_cell/<id>',             views.GridCellSingle.as_view(),  name='cell'),
    path('grid_cell/<id>/forecasts/',  views.ForecastList.as_view(),    name='forecasts'),
]
