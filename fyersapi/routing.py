from django.urls import re_path
from .consumers import FyersPositionDataConsumer, FyersIndexDataConsumer
from channels.routing import ProtocolTypeRouter, URLRouter

ws_urlpatterns = [
    # WebSocket route for FyersIndexDataConsumer with a dynamic parameter 'last_keyword'
    re_path(r'^ws/fyersindexdata/(?P<last_keyword>\w+)/$', FyersIndexDataConsumer.as_asgi()),

    # WebSocket route for FyersPositionDataConsumer
    re_path(r'^ws/fyerspositionsdata/$', FyersPositionDataConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    # WebSocket protocol router
    "websocket": URLRouter(ws_urlpatterns),
})
