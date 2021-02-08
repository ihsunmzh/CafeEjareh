# Generated by Django 2.2 on 2020-10-03 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50, null=True, verbose_name='نام کامل')),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='ایمیل')),
                ('text', models.TextField(null=True, verbose_name='متن')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ ساخته شدن')),
            ],
            options={
                'verbose_name': 'تماس با ما',
                'verbose_name_plural': 'تماس با ما',
                'ordering': ('-created_at',),
            },
        ),
    ]