# Generated by Django 2.2 on 2020-10-11 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(blank=True, choices=[('f', 'زن'), ('m', 'مرد')], max_length=1, null=True),
        ),
    ]