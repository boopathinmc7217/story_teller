from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Stories(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.TextField()
    path = models.FilePathField(default="data")
