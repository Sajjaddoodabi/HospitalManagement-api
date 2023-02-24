import datetime

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models

# departments = [('General', 'General'),
#                ('Cardiologist', 'Cardiologist'),
#                ('Dermatologists', 'Dermatologists'),
#                ('Emergency Medicine Specialists', 'Emergency Medicine Specialists'),
#                ('Allergists/Immunologists', 'Allergists/Immunologists'),
#                ('Anesthesiologists', 'Anesthesiologists'),
#                ('Colon and Rectal Surgeons', 'Colon and Rectal Surgeons')
#                ]
Patient_status = []

Insurance_status = [('VLD', 'valid'),
                    ('NVD', 'not valid')]

DOCTOR_STATUS = (('ACP', 'accepted'),
                 ('DEC', 'declined'),)


class UserManagement(BaseUserManager):
    def create_user(self, username, email, is_active=True, is_staff=False, password=None):
        if not password:
            raise ValueError('password is required!')
        if not email:
            raise ValueError('email is required!')

        user_obj = self.model(email=email, username=username)

        user_obj.password = make_password(password)
        user_obj.staff = is_staff
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, username, email, password=None):
        user_obj = self.create_user(email=email, username=username, password=password)
        user_obj.is_staff = True
        user_obj.is_superuser = True
        user_obj.role = 'ADM'
        user_obj.save(using=self._db)
        return user_obj


class BaseUser(AbstractUser):
    Roles = (('DOC', 'doctor'),
             ('PAT', 'patient'),
             ('ADM', 'admin'))

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
    email = models.EmailField(unique=True)
    status = models.BooleanField(default=True)

    objects = UserManagement()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = 'BaseUser'
        verbose_name_plural = 'BaseUsers'
        db_table = 'BaseUser'

    @property
    def get_name(self):
        if self.username is not None:
            return self.username
        else:
            return f'{self.first_name} {self.last_name}'


class DoctorCategory(models.Model):
    title = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Insurance(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(max_length=500)
    reduce_percent = models.IntegerField()
    status = models.CharField(choices=Insurance_status, max_length=300, default='NVD')

    def __str__(self):
        return self.title


class Doctor(models.Model):
    parent_user = models.OneToOneField(BaseUser, related_name='doctor', on_delete=models.CASCADE)
    category = models.ForeignKey(DoctorCategory, on_delete=models.CASCADE, related_name='doctor')
    address = models.CharField(max_length=300, null=True, blank=True)
    doctor_status = models.CharField(choices=DOCTOR_STATUS, max_length=60, default='DEC')

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'

    def __str__(self):
        return f'{self.parent_user.get_name} - {self.category}'


class Patient(models.Model):
    parent_user = models.OneToOneField(BaseUser, related_name='patient', on_delete=models.CASCADE)
    insurance = models.ForeignKey(
        Insurance,
        on_delete=models.CASCADE,
        related_name='patient',
        blank=True,
        null=True
    )
    symptoms = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        verbose_name = 'patient'
        verbose_name_plural = 'patients'

    def __str__(self):
        return f'{self.parent_user.get_name}'
