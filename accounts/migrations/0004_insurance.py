# Generated by Django 4.1.6 on 2023-02-24 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_doctor_doctor_status_alter_doctorcategory_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='insurance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('description', models.TextField(max_length=500)),
                ('reduce_percent', models.IntegerField()),
                ('status', models.CharField(choices=[('VLD', 'valid'), ('NVD', 'not valid')], default='NVD', max_length=300)),
            ],
        ),
    ]
