from django.db import models

from accounts.models import Patient, Doctor

STATUS = (('DEN', 'denied'),
          ('ACP', 'accepted'),
          ('DON', 'done'),
          ('DO', 'doing'),
          ('QUE', 'in-queue'),)


class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescription')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='prescription')
    description = models.TextField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(choices=STATUS, max_length=50, default='QUE')

    def __str__(self):
        return f'{self.patient} - {self.doctor}'


class Medicine(models.Model):
    title = models.CharField(max_length=200)
    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name='medicine',
        null=True,
        blank=True
    )
    count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
