from django.urls import path
from .views import *

urlpatterns = [
    path('detectme2', detectme2, name="detectme2"),
]