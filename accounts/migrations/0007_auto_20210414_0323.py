# Generated by Django 3.1.5 on 2021-04-13 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20210414_0137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phoneotp',
            name='username',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
    ]
