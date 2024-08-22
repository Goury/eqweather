from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include('api.urls', namespace='api')),
    path('admin/', admin.site.urls),
]
