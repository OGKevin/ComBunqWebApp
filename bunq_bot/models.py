from django.db import models
from django.utils import timezone
# Create your models here.


class ChatInfo(models.Model):

    chat_id = models.CharField(max_length=20, null=True, blank=True)


class BunqTogether(models.Model):

    title = models.CharField(max_length=150, null=True, blank=True)


class BunqNews(models.Model):

    title = models.CharField(max_length=150, null=True, blank=True)
    author = models.CharField(max_length=150, null=True, blank=True)
    date = models.DateTimeField(blank=True, null=True,
                                default=timezone.now)
