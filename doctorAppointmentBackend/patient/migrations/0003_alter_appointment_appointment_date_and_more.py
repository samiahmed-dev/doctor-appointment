# Generated by Django 4.2.6 on 2024-06-18 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_alter_patientprofile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='appointment_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='appointment_time',
            field=models.TimeField(),
        ),
    ]
