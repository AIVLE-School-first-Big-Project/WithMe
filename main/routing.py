from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/service/(?P<user_log>\w+)/$', consumers.ChatConsumer.as_asgi()),
]