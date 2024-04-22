from django.urls import path
from .auth import login, register, profile


urlpatterns = [
    path('auth/login/',login.login_view.as_view(),name='login'),
    path('auth/register/',register.register_view.as_view(),name='register'),
    path('profile/',profile.profile_view.as_view(),name='profile'),
]