from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManagement(BaseUserManager):
    def create_user(self, email, is_active=True, is_staff=False, password=None):
        if not password:
            raise ValueError('password is required!')
        if not email:
            raise ValueError('email is required!')

        user_obj = self.model(email=email)

        user_obj.password = make_password(password)
        user_obj.staff = is_staff
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, email, password=None):
        user_obj = self.model(email=email, password=password)
        user_obj.is_staff = True
        user_obj.is_superuser = True
        user_obj.save(using=self._db)
        return user_obj


class BaseUser(AbstractUser):
    Roles = (('DOC', 'doctor'),
             ('RES', 'receptionist'),
             ('PAT', 'patient'))

    profile_image = models.ImageField(
        verbose_name='Image',
        upload_to='images/',
        default='images.Default.png'
    )
    alt_text = models.CharField(
        verbose_name='Alternative Text',
        max_length=255,
        null=True,
        blank=True
    )
    role = models.CharField(choices=Roles, max_length=20, default='PAT')
    mobile = models.CharField(max_length=20)
    status = models.BooleanField(default=False)

    objects = UserManagement()

    @property
    def get_name(self):
        if self.first_name and self.last_name is not None:
            return f'{self.first_name} {self.last_name}'
        else:
            return self.email


class Doctor(BaseUser):
    departments = [('General', 'General'),
                   ('Cardiologist', 'Cardiologist'),
                   ('Dermatologists', 'Dermatologists'),
                   ('Emergency Medicine Specialists', 'Emergency Medicine Specialists'),
                   ('Allergists/Immunologists', 'Allergists/Immunologists'),
                   ('Anesthesiologists', 'Anesthesiologists'),
                   ('Colon and Rectal Surgeons', 'Colon and Rectal Surgeons')
                   ]

    department = models.CharField(choices=departments, max_length=20, default='General')
    address = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.get_name()


class Patient(BaseUser):
    symptoms = models.CharField(max_length=200, null=False)
    address = models.CharField(max_length=300)

    def __str__(self):
        return self.get_name()


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
