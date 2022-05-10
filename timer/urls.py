from django.urls import path
from . import views

app_name = 'timer'

urlpatterns = [
    path('service', views.service, name='main'),
    path('result', views.result, name='result'),
    path('result_item', views.test_result, name='result_item'),
]
