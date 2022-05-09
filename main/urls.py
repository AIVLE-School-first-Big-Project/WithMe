from django.urls import path, re_path
from .views import *
from timer.views import service
urlpatterns = [
    path('', service, name='service'),
    path('detectme', detectme, name="detectme"),

    # push
    path('pushmes/', pushmes, name='pushmes'),
]