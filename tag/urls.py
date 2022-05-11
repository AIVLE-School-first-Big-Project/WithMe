from .views import Autocomplete, BasicDALView
from django.urls import path

urlpatterns = [
    path('test/', Autocomplete.as_view(), name='test'),
    path('test2/', BasicDALView, name='test2'),

]
