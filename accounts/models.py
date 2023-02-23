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


# Times = [('9', '9'),
#          ('9:30', '9:30'),
#          ('10', '10'),
#          ('10:30', '10:30'),
#          ('11', '11'),
#          ('11:30', '11:30'),
#          ('12', '12'),
#          ('12:30', '12:30'), ]


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


class DoctorCategory(models.Model):
    title = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Doctor(models.Model):
    parent_user = models.OneToOneField(BaseUser, related_name='doctor', on_delete=models.CASCADE)
    category = models.ForeignKey(DoctorCategory, on_delete=models.CASCADE, related_name='doctor')
    address = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'

    @property
    def get_name(self):
        if self.parent_user.username is not None:
            return self.parent_user.username
        else:
            return f'{self.parent_user.first_name} {self.parent_user.last_name}'

    def __str__(self):
        return f'{self.get_name} - {self.category}'


class Patient(models.Model):
    parent_user = models.OneToOneField(BaseUser, related_name='patient', on_delete=models.CASCADE)
    symptoms = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)

    # insurance = models.CharField(max_length=400, blank=True, null=True)

    class Meta:
        verbose_name = 'patient'
        verbose_name_plural = 'patients'

    @property
    def get_name(self):
        if self.parent_user.username is not None:
            return self.parent_user.username
        else:
            return f'{self.parent_user.first_name} {self.parent_user.last_name}'

    def __str__(self):
        return f'{self.get_name}'
