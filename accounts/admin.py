from django.contrib import admin

from Hospital.models import TimesForTheDay
from .models import *


class TimesAdmin(admin.TabularInline):
    model = TimesForTheDay


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    inlines = [
        TimesAdmin,
    ]


admin.site.register(BaseUser)
admin.site.register(Patient)
admin.site.register(DoctorCategory)
