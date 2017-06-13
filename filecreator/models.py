from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist


# Create your models here.
class Tokens(models.Model):
    """docstring for Profile."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file_token = models.CharField(blank=True, max_length=150)


@receiver(post_save, sender=User)
def create_user_tokens(sender, instance, created, **kwargs):
    if created:
        Tokens.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_tokens(sender, instance, **kwargs):
    try:
        instance.tokens.save()
    except ObjectDoesNotExist:  # pragma: no cover
        Tokens.objects.create(user=instance)
