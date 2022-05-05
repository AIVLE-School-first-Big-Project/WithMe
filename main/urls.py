from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('settings', settings, name='settings'),
    path('detectme', detectme, name="detectme"),

    path('camera_setting', camera_setting, name="camera_setting"),

    # push
    path('pushmes/', pushmes, name='pushmes'),
]