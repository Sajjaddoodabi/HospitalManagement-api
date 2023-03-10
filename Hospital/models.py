import datetime

from django.db import models
from accounts.models import Doctor, Patient

STATUS = (('DEC', 'declined'),
          ('ACP', 'accepted'),
          ('DON', 'done'),
          ('DO', 'doing'),
          ('QUE', 'in-queue'),)


class AppointmentTime(models.Model):
    time = models.CharField(max_length=20)
    is_active = models.BooleanField()

    def __str__(self):
        return self.time


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointment')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointment')
    appointment_time = models.ForeignKey(AppointmentTime, on_delete=models.CASCADE, related_name='appointment')
    day = models.DateField(default=datetime.date.today())
    description = models.TextField(max_length=500, blank=True, null=True)
    status = models.CharField(choices=STATUS, max_length=50, default='QUE')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.doctor.parent_user.get_name} - {self.patient.parent_user.get_name} - {self.appointment_time}'


class TimesForTheDay(models.Model):
    Doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='time_for_day')
    times = models.ForeignKey(AppointmentTime, on_delete=models.CASCADE, related_name='time_for_day')
    day = models.DateField(default=datetime.date.today())

    def __str__(self):
        return f'{self.Doctor.parent_user.get_name} - {self.times}'
