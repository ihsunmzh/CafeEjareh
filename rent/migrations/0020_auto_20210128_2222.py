# Generated by Django 2.2 on 2021-01-28 22:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0019_auto_20210128_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 27, 22, 22, 57, 959305), verbose_name='زمان انقضا'),
        ),
    ]
