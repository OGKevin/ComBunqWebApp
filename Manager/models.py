from __future__ import unicode_literals
from django.contrib.postgres.fields import ArrayField
from django.db import models
from simple_history.models import HistoricalRecords

# Create your models here


class catagories(models.Model):
    Naam = models.CharField(max_length=20)
    Rekening = ArrayField(models.CharField(
        max_length=34), blank=True, null=True)
    regex = ArrayField(models.CharField(max_length=50, blank=True, null=True))
    history = HistoricalRecords()

    def __str__(self):  # pragma: no cover
        return self.Naam
