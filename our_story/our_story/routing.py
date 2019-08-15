from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import app_chat.routing, app_dashboard.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            app_chat.routing.websocket_urlpatterns + app_dashboard.routing.websocket_urlpatterns
        )
    ),
})