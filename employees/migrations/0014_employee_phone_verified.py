# Generated by Django 3.1.5 on 2021-04-13 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0013_employee_subscription_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='phone_verified',
            field=models.BooleanField(default=False),
        ),
    ]
