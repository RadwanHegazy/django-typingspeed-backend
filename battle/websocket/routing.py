from django.urls import re_path
from .consumers import SearchBattle

ws_urlpatterns = [
    re_path('ws/battle/search/',SearchBattle.as_asgi()),
]