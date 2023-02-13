from django.db import models

from accounts.models import Doctor, Patient


class Appointments(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointment')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointment')
    time = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.doctor.get_name()} - {self.patient.get_name()}'


class Reception(models.Model):
    appointment = models.ForeignKey(Appointments, on_delete=models.CASCADE, related_name='receptionist')

    def __str__(self):
        return self.appointment
