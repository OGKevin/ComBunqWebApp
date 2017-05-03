from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Profile(models.Model):
    """docstring for Profile.

    This model gives each user all these fields except 'user'.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    GUID = models.CharField(blank=True, max_length=68)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
