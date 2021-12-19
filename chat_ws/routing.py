from django.urls import  path

from .consumers import ChatConsumer

ws_urlpatterns = [
    path('ws/some_url', ChatConsumer.as_asgi()),
    # path('ws/some_url', ChatConsumer),
]
