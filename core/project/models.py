from django.contrib import admin
from django.db import models
from django.utils import timezone


class Message(models.Model):
    message_text = models.TextField()
    pub_date = models.DateTimeField("Date", default=timezone.now)

    def __str__(self):
        return self.message_text


class Response(models.Model):
    question = models.ForeignKey(Message, models.CASCADE, related_name="responses")
    response_text = models.TextField()
    # attached_file = models.FileField(upload_to=...)
    completion_tokens = models.PositiveIntegerField()
    prompt_tokens = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=6)

    def __str__(self):
        return self.response_text

    def total_tokens(self):
        return self.prompt_tokens + self.completion_tokens
