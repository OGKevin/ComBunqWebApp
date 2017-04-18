from django.contrib import admin
from .models import catagories
from .forms import catagoriesAdminForm
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.


@admin.register(catagories)
class catagoriesAdmin(SimpleHistoryAdmin):
    form = catagoriesAdminForm
