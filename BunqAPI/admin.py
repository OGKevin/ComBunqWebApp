from django.contrib import admin
from .models import Profile
# Register your models here.


@admin.register(Profile)
class pofile_admin(admin.ModelAdmin):
    """docstring for pofile_admin."""
    pass
