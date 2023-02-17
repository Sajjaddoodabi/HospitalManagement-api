from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models

departments = [('General', 'General'),
               ('Cardiologist', 'Cardiologist'),
               ('Dermatologists', 'Dermatologists'),
               ('Emergency Medicine Specialists', 'Emergency Medicine Specialists'),
               ('Allergists/Immunologists', 'Allergists/Immunologists'),
               ('Anesthesiologists', 'Anesthesiologists'),
               ('Colon and Rectal Surgeons', 'Colon and Rectal Surgeons')
               ]
Patient_status = []
Times = [('9', '9'),
         ('9:30', '9:30'),
         ('10', '10'),
         ('10:30', '10:30'),
         ('11', '11'),
         ('11:30', '11:30'),
         ('12', '12'),
         ('12:30', '12:30'), ]


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

    @property
    def get_name(self):
        if self.first_name and self.last_name is not None:
            return f'{self.first_name} {self.last_name}'
        else:
            return self.username

    class Meta:
        verbose_name = 'BaseUser'
        verbose_name_plural = 'BaseUsers'
        db_table = 'BaseUser'


class Doctor(BaseUser):
    department = models.CharField(choices=departments, max_length=40, default='General')
    address = models.CharField(max_length=300, null=True, blank=True)
    times = models.CharField(choices=Times, max_length=30, default='9')

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'

    def __str__(self):
        return f'{self.get_name} - {self.department}'


class Patient(BaseUser):
    requested_doctor = models.CharField(choices=departments, max_length=40, default='General')
    symptoms = models.CharField(max_length=200)
    address = models.CharField(max_length=300)

    class Meta:
        verbose_name = 'patient'
        verbose_name_plural = 'patients'

    def __str__(self):
        return f'{self.get_name} - {self.requested_doctor}'
