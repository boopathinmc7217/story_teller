from rest_framework import serializers
from .models import Stories
class StoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stories
        field = ("user","topic","path")