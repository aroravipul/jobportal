# Generated by Django 3.1.5 on 2021-02-27 21:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_name', models.CharField(max_length=20)),
                ('job_category', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firm_name', models.CharField(max_length=50)),
                ('firm_category', models.CharField(max_length=50)),
                ('full_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('no_of_requirments', models.IntegerField(default=1)),
                ('salary_offered', models.IntegerField()),
                ('shift_offered', models.CharField(choices=[('day', 'Day'), ('night', 'Night')], default='Day', max_length=10)),
                ('match_otp', models.IntegerField(blank=True, null=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('is_published', models.BooleanField(default=False)),
                ('discount', models.FloatField()),
                ('subscription', models.CharField(choices=[('1month', '999/One Month/10 Contacts'), ('2month', '1299/Two Month/10 Contacts')], default='999/One Month/10 Contacts', max_length=50)),
                ('requirement', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='employers.job')),
            ],
        ),
    ]
