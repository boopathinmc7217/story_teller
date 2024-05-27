from django.urls import path
from .views import get_story, login, my_stories, register, logout, story_url, home
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("get_story", get_story, name="get_story"),
    path("signup", register, name="signup"),
    path("login", login, name="login"),
    path("logout", logout),
    path("my_stories", my_stories),
    path("story_url/<int:story_id>", story_url, name="story_url"),
    path("home", home, name="home"),
]
