# Generated by Django 4.0.7 on 2022-09-15 08:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_coin_update_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coin',
            name='update_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 9, 15, 8, 56, 37, 190685, tzinfo=utc)),
        ),
    ]