# Generated by Django 4.1.6 on 2023-02-17 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_patient_requested_department'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patient',
            old_name='requested_department',
            new_name='requested_doctor',
        ),
    ]
