# Generated by Django 5.0.6 on 2024-06-07 06:07

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("food", "0004_item_user_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="time_stamp",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
