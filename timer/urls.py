from django.urls import path
from . import views

app_name = 'timer'

urlpatterns = [
    path("watch/", views.watch, name='watch'),
    path("timer/", views.timer, name='timer'),
    path("stopwatch/", views.stopwatch, name='stopwatch'),
]