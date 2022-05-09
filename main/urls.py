from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', camera_setting, name='camera_setting'),
    path('detectme', detectme, name="detectme"),

    # push
    path('pushmes/', pushmes, name='pushmes'),
]