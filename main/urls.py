from django.urls import path, re_path
from .views import *
from timer.views import service
urlpatterns = [
    path('', service, name='service'),
    path('mypage', mypage, name="mypage"),
    path('detectme', detectme, name="detectme"),

]