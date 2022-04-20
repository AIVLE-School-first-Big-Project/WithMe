from django.urls import path, re_path
from .views import index

urlpatterns = [
    path('', index, name='index')
]