from django.contrib import admin

from Hospital.models import Appointment, AppointmentTime, TimesForTheDay

admin.site.register(Appointment)
admin.site.register(AppointmentTime)
admin.site.register(TimesForTheDay)