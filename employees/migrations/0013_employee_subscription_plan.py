# Generated by Django 3.1.5 on 2021-04-10 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_subscription_employee_subscription_employer'),
        ('employees', '0012_auto_20210411_0325'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='subscription_plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.subscription_employee'),
        ),
    ]
