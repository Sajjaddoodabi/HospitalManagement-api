# Generated by Django 4.1.6 on 2023-02-17 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_baseuser_options_alter_baseuser_table'),
        ('Hospital', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Appointments',
            new_name='Appointment',
        ),
    ]