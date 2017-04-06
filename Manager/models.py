from __future__ import unicode_literals
from django.contrib.postgres.fields import JSONField
from django.db import models

# Create your models here.
class transactions(models.Model):
    """docstring for transactions."""
    attrs = JSONField()
    catagory = JSONField()
        
