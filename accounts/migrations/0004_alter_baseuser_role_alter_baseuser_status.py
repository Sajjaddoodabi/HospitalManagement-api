# Generated by Django 4.1.6 on 2023-02-17 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_baseuser_options_alter_baseuser_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseuser',
            name='role',
            field=models.CharField(choices=[('DOC', 'doctor'), ('PAT', 'patient'), ('ADM', 'admin')], default='PAT', max_length=20),
        ),
        migrations.AlterField(
            model_name='baseuser',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]