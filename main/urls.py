from django.urls import path, re_path
from .views import index, settings

urlpatterns = [
    path('', index, name='index'),
    path('settings', settings, name='settings')
]