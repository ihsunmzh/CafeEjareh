# Generated by Django 2.2 on 2021-01-31 19:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0020_auto_20210128_2222'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='ratings',
            new_name='rating',
        ),
        migrations.AlterField(
            model_name='rent',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 2, 19, 15, 33, 704977), verbose_name='زمان انقضا'),
        ),
    ]
