from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/service/(?P<user_log>\w+)/$', consumers.PredictConsumer.as_asgi()),
    re_path(r'ws/service2/(?P<user_log>\w+)/$', consumers.PredictConsumer2.as_asgi()),
]
