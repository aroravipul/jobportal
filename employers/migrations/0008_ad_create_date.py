# Generated by Django 3.1.5 on 2021-04-06 21:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employers', '0007_auto_20210402_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
