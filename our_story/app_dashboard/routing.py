from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('<str:my_username>/', consumers.DashConsumer),
]