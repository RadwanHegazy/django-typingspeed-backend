from django.urls import path
from .consumers import SearchBattle, BattleConsumer

websocket_urlpatterns = [
    path('ws/battle/search/',SearchBattle.as_asgi()),
    path('ws/battle/get/<str:battle_id>/',BattleConsumer.as_asgi()),
]