from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('settings', settings, name='settings'),
    path('detectme', detectme, name="detectme"),
    path('camera', camera_test, name="camera_test"),

    # push
    path('pushmes/', pushmes, name='pushmes'),

]