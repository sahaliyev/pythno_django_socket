from django.conf.urls import url

from .consumers import ChatConsumer

websocket_urlpatterns = [
    url('details/<int:post_id>/', ChatConsumer)
]
