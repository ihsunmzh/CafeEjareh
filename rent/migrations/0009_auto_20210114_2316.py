# Generated by Django 2.2 on 2021-01-14 19:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0008_auto_20210114_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 13, 19, 46, 50, 828393, tzinfo=utc), verbose_name='زمان انقضا'),
        ),
    ]
