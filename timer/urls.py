from django.urls import path
from . import views
from tag.views import Autocomplete, BasicDALView
app_name = 'timer'

urlpatterns = [
    path("watch/", views.watch, name='watch'),
    path("timer/", views.timer, name='timer'),
    path("stopwatch/", views.stopwatch, name='stopwatch'),
    path("create_timelog/", views.create_timelog, name='create_timelog'),
    path("create_userlog/", views.create_userlog, name='create_userlog'),

    path('service', views.service, name='main'),
]