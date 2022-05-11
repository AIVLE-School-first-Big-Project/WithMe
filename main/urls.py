from django.urls import path
from .views import mypage, detectme
from timer.views import service

urlpatterns = [
    path('', service, name='service'),
    path('mypage', mypage, name="mypage"),
    path('detectme', detectme, name="detectme"),

]
