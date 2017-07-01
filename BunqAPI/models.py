from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
# Create your models here.


class Session(models.Model):
    """docstring for Session.

    This model gives each user all these fields except 'user'.
    Not sure how long the session_token actaully is.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    session_token = models.CharField(blank=True, max_length=150)
    session_user_id = models.CharField(blank=True, max_length=150)
    # NOTE: user_id should be stored in session_token
    # NOTE: These below are not webClient session keys

    session_end_date = models.DateTimeField(blank=True, null=True,
                                            default=timezone.now)
    session_server_id = models.CharField(blank=True, null=True, max_length=150)
    session_server_token = models.CharField(blank=True, null=True,
                                            max_length=150)
    new_id = models.CharField(blank=True, null=True, max_length=150)
    old_id = models.CharField(blank=True, null=True, max_length=150)


@receiver(post_save, sender=User)
def create_user_session(sender, instance, created, **kwargs):
    if created:
        Session.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_session(sender, instance, **kwargs):
    try:
        instance.session.save()
    except ObjectDoesNotExist:  # pragma: no cover
        Session.objects.create(user=instance)
