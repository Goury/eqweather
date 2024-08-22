from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    path('', views.api_root),
    path('grid_cell/',                 views.GridCellList.as_view(),         name='cells'),
    path('grid_cell/<id>',             views.GridCellSingle.as_view(),       name='cell'),
    path('grid_cell/<id>/forecasts/',  views.ForecastList.as_view(),         name='forecasts'),
    path('forecasts/<datetime>/',      views.ForecastPerTimeList.as_view(),  name='forecasts-per-time'),
    path('times/',                     views.TimesList.as_view(),            name='times'),
]
