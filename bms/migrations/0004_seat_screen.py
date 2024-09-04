# Generated by Django 5.1 on 2024-09-03 15:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bms', '0003_screenfeature'),
    ]

    operations = [
        migrations.AddField(
            model_name='seat',
            name='screen',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='bms.screen'),
        ),
    ]
