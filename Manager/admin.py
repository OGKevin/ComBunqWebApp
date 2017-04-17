from django.contrib import admin
from .models import catagories
from .forms import catagoriesAdminForm

# Register your models here.


class catagoriesAdmin(admin.ModelAdmin):
    form = catagoriesAdminForm


admin.site.register(catagories, catagoriesAdmin)
