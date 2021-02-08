from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
	""" My Customized User Model. """

	SEX_TYPE = (
		('f', 'زن'),
		('m', 'مرد'),
	)

	username = models.CharField(max_length=64,unique=True, null=True, blank=True)
	email = models.EmailField(unique=True, verbose_name='ایمیل', null = True)
	
	bio = models.TextField(verbose_name = 'سایر اطلاعات', null=True, blank=True)
	birthdate = models.DateField(max_length = 150, null=True, blank=True)
	sex = models.CharField(max_length=1, choices=SEX_TYPE, null=True, blank=True)
	
	home_address = models.TextField(verbose_name = 'آدرس خانه', null=True, blank=True)
	home_phone_number = models.CharField(max_length = 32, verbose_name = 'شماره موبایل', null=True, blank=True)
	mobile_number = models.CharField(max_length = 32, verbose_name = 'شماره موبایل', null=True, blank=True)
	
	avatar = models.ImageField(upload_to='uploads/avatars/%Y-%m-%d/', verbose_name = 'تصویر پروفایل', null=True, blank=True)
	
	state = models.CharField(max_length = 32, verbose_name = 'استان', null=True, blank=True)
	city = models.CharField(max_length = 32, verbose_name = 'شهر', null=True, blank=True)

	is_author = models.BooleanField(default=False, verbose_name="وضعیت نویسندگی")
	is_block = models.BooleanField(default=False, verbose_name="وضعیت بلاک کاربر")
	special_user = models.DateTimeField(default=timezone.now, verbose_name="کاربر ویژه تا")

	def is_special_user(self):
		if self.special_user > timezone.now():
			return True
		else:
			return False
	is_special_user.boolean = True
	is_special_user.short_description = "وضعیت کاربر ویژه"

	def __str__(self):
		return self.username
