from django.urls import path
from . import views

app_name = 'timer'

urlpatterns = [
    path("timer/", views.watch, name='timer'),
    
]