
from django.urls import path,include
from .views import get_story
urlpatterns = [
    path("get_story",get_story)
]
