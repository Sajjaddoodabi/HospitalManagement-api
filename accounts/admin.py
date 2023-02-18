from django.contrib import admin
from .models import *


class TimesAdmin(admin.TabularInline):
    model = TimesForTheDay


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    inlines = [
        TimesAdmin
    ]


admin.site.register(BaseUser)
admin.site.register(Patient)
