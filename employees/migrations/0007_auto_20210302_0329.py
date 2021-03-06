# Generated by Django 3.1.5 on 2021-03-01 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0006_auto_20210302_0249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='exp_salary_frequency',
            field=models.CharField(choices=[('Hourly', 'Hourly'), ('Daily', 'Daily'), ('Monthly', 'Monthly')], default='Monthly', max_length=20),
        ),
        migrations.AlterField(
            model_name='employee',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], max_length=10),
        ),
    ]
