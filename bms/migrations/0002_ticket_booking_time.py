# Generated by Django 5.1 on 2024-09-01 12:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='booking_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
