from django.urls import re_path

from . import consumers

ws_urlpatterns = [
    re_path(r'ws/tracking/(?P<tracking_code>\w+)/$', consumers.TrackingDetailConsumer.as_asgi())
    # path('ws/tracking/<str:tracking_code>/', consumers.TrackingDetailConsumer.as_asgi())
]