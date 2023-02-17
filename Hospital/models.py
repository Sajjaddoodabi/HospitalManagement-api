from django.db import models

from accounts.models import Doctor, Patient, Times


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointment')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointment')
    time = models.DateTimeField(auto_now_add=True)
    appointment_time = models.CharField(choices=Times, max_length=40, default='9')
    description = models.TextField(max_length=500, blank=True, null=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.doctor.get_name()} - {self.patient.get_name()}'


# class Reception(models.Model):
#     appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='receptionist')
#
#     def __str__(self):
#         return self.appointment
