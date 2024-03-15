import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chatapp.routing import websocket_urlspattern


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = ProtocolTypeRouter({
                    "http": get_asgi_application(),
                    "websocket": AuthMiddlewareStack(URLRouter(
                        websocket_urlspattern
                        )
                    )
                }
            )
