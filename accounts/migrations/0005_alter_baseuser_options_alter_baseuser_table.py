# Generated by Django 4.1.6 on 2023-02-17 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_baseuser_role_alter_baseuser_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='baseuser',
            options={'verbose_name': 'BaseUser', 'verbose_name_plural': 'BaseUsers'},
        ),
        migrations.AlterModelTable(
            name='baseuser',
            table='BaseUser',
        ),
    ]
