# Generated by Django 3.2 on 2021-04-28 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0014_employee_phone_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='subscription_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
