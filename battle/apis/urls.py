from django.urls import path
from .views import get, create

urlpatterns = [
    path('get/<str:battle_id>/',get.get_battle.as_view(),name='get_battle'),
    path('create/',create.create_battle.as_view(),name='create_battle'),
]