# Generated by Django 2.2 on 2021-01-13 01:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 12, 1, 6, 55, 594774, tzinfo=utc), verbose_name='زمان انقضا'),
        ),
    ]
