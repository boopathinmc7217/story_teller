from django.urls import path
from .views import get_story, login, register, logout
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("get_story", get_story),
    path("signup", register),
    path("login", login),
    path("logout", logout),
]
