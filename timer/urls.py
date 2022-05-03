from django.urls import path
from . import views
from tag.views import Autocomplete, BasicDALView
app_name = 'timer'

urlpatterns = [
    path("watch/", views.watch, name='watch'),
    path("timer/", views.timer, name='timer'),
    path("stopwatch/", views.stopwatch, name='stopwatch'),
    path("set_start_time/", views.set_start_time, name='set_start_time'),
]