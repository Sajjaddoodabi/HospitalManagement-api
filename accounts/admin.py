from django.contrib import admin
from .models import *


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('department',)


admin.site.register(BaseUser)
admin.site.register(Patient)
