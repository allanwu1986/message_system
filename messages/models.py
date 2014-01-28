from django.db import models
from django.contrib.auth.models import User

class CachedMessage(models.Model):
    writer = models.ForeignKey(User)
    message = models.CharField(max_length=1024)

class UserMessage(models.Model):
    read = models.BooleanField(default=False)
    message = models.IntegerField()

class Inbox(models.Model):
    owner = models.ForeignKey(User,unique=True)
    messages = models.ManyToManyField(UserMessage)


