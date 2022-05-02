from django.urls import path
from .views import *

urlpatterns = [
    path('', timer2, name='timer2'),
]