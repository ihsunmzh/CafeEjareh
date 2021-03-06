# Generated by Django 2.2 on 2021-01-17 23:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rent', '0014_auto_20210117_2321'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('type_order', models.CharField(blank=True, max_length=100, null=True, verbose_name='نوع سفارش')),
                ('status', models.CharField(choices=[('payment', 'payment'), ('unpaid', 'unpaid')], default='unpaid', max_length=20, verbose_name='وضعیت سفارش')),
                ('refid', models.IntegerField(blank=True, default=0, null=True, verbose_name='شماره پیگیری تراکنش')),
                ('total', models.IntegerField(blank=True, default=0, null=True, verbose_name=' مبلغ سفارش')),
                ('statuscode', models.IntegerField(blank=True, null=True, verbose_name='کد وضعیت')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربری سفارش')),
                ('rent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rent.Rent', verbose_name=' آگهی')),
            ],
        ),
    ]
