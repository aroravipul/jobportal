# Generated by Django 3.1.5 on 2021-04-11 00:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers', '0002_auto_20210301_1834'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='volunteer',
            name='no_of_registrations',
        ),
    ]
