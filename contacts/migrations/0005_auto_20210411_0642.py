# Generated by Django 3.1.5 on 2021-04-11 01:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0004_auto_20210410_0358'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee_to_employer',
            old_name='employee_phone',
            new_name='employer_phone',
        ),
        migrations.RenameField(
            model_name='employer_to_employee',
            old_name='employer_phone',
            new_name='employee_phone',
        ),
    ]