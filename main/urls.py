from django.urls import path, re_path
from .views import index, settings, detectme

urlpatterns = [
    path('', index, name='index'),
    path('settings', settings, name='settings'),
    path('detectme', detectme, name="detectme"),
]