from django.urls import path
from .views import detectme2, detectneck

urlpatterns = [
    path('detectme2', detectme2, name="detectme2"),
    path('detectneck', detectneck, name='detectneck')
]
