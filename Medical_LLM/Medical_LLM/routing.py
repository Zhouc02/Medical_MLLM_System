# routing.py

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.YourConsumer.as_asgi()),
    re_path(r'ws/chat2/doctors/$', consumers.DoctorsConsumer.as_asgi()),
]
