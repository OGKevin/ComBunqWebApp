from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField
# Create your models here.


class Profile(models.Model):
    """docstring for Profile.

    This model gives each user all these fields except 'user'.
    Not sure how long the session_token actaully is.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    GUID = ArrayField(
        models.CharField(
            max_length=68,
            blank=True,
        ),
        default=['No GUI yet'],
        blank=True,
        null=True
    )
    session_token = models.CharField(blank=True, max_length=150)
    invoice_token = models.CharField(blank=True, max_length=150)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Proxy(models.Model):
    """docstring for Proxy."""
    proxy_uri = models.CharField(blank=True, max_length=50)

    def __str__(self):  # pragma: no cover
        return self.proxy_uri
