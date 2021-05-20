from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
# from delivery.consumers import  PackageConsumer
from django.conf.urls import url
from .token_auth_middleware import TokenAuthMiddleware
 
application = ProtocolTypeRouter(
    {
        # (http->django views is added by default)
        "websocket": TokenAuthMiddleware(
            URLRouter([
                #  url('ws/package', PackageConsumer.as_asgi()),
            ])
            
        )
    }
)
