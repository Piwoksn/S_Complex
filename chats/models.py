from django.db import models
from myapp.models import User
# Create your models here.


class SentChats(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    receiver = models.EmailField(null=True, blank=True)
    # receivedmessages = models.TextField(null=True, blank=True)
    sentmessages = models.TextField(null=True, blank=True)
    timesent = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.receiver
