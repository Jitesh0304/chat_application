from django.db import models
from registration.models import User



class Chat(models.Model):
    senduser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="message_sender")
    content = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now=True)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)


class Group(models.Model):
    name = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now=True)
    members = models.ManyToManyField(User, blank=False, related_name='group_members')