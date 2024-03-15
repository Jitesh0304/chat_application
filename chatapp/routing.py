from .consumers import MyAsyncJsonWebsocketConsumer
from django.urls import path


websocket_urlspattern = [
    path('ws/awsc/<str:groupname>/', MyAsyncJsonWebsocketConsumer.as_asgi())
]