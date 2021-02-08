# Generated by Django 2.2 on 2021-01-14 19:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0003_auto_20210113_0457'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rent',
            name='created',
        ),
        migrations.AlterField(
            model_name='rent',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 13, 19, 22, 23, 310173, tzinfo=utc), verbose_name='زمان انقضا'),
        ),
        migrations.AlterField(
            model_name='rent',
            name='price',
            field=models.DecimalField(decimal_places=100, max_digits=100, null=True, verbose_name='قیمت'),
        ),
    ]
