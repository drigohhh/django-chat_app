from django.contrib import admin
from django.db import models
from django.utils import timezone


class Message(models.Model):
    message_text = models.CharField(max_length=256)
    pub_date = models.DateTimeField("Date", default=timezone.now)

    def __str__(self):
        return self.message_text
