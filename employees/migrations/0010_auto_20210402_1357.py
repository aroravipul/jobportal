# Generated by Django 3.1.5 on 2021-04-02 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0009_auto_20210330_0310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='pref_shift',
            field=models.CharField(choices=[('Day', 'Day'), ('Night', 'Night'), ('Any', 'Any')], default='Day', max_length=20),
        ),
        migrations.AlterField(
            model_name='employee',
            name='prev_work_exp',
            field=models.CharField(default='Fresher', max_length=100),
        ),
    ]
