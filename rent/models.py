from django.db import models
from django.db.models import Avg

from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import slugify

from painless.jalali_date.utils import jalali_converter 

from django.contrib.contenttypes.fields import GenericRelation

from ckeditor.fields import RichTextField

from rent.managers import CategoryManager
from rent.managers import CommentManager
from rent.managers import RentManager

from accounts.models import User
from hitcount.models import HitCountMixin, HitCount
from mptt.models import MPTTModel, TreeForeignKey
from star_ratings.models import Rating

from django.shortcuts import reverse

import datetime


@python_2_unicode_compatible
class Rent(models.Model):
	""" Model definition for Rent-Ads. """

	STATUS_CHOICES = (
		('d', 'پیش‌نویس'),		  # draft
		('p', "منتشر شده"),		 # publish
		('i', "در حال بررسی"),	 # investigation
		('b', "برگشت داده شده"), # back
	)

	RENT_TYPE = (
		('h', 'ساعتی'),
		('d', 'روزانه'),
		('w', 'هفتگی'),
		('m', 'ماهیانه'),
		('y', 'سالیانه'),
	)

	title = models.CharField(max_length=128, verbose_name = 'عنوان', null=True)
	slug = models.SlugField(allow_unicode = True, verbose_name = 'مسیر آدرس دهی', null=True) 
	description = models.TextField(null=True, verbose_name='توضیحات')
	category = TreeForeignKey('Category', related_name='category_rent', on_delete = models.CASCADE, null=True)
	
	state = models.ForeignKey('State', on_delete = models.CASCADE, null=True)
	city = models.ForeignKey('City', on_delete = models.CASCADE, null=True)
	author = models.ForeignKey(User, related_name = 'author_rent', verbose_name = 'نویسنده', on_delete = models.CASCADE, null=True)
	
	mobile_number = models.CharField(max_length = 32, verbose_name = 'شماره موبایل', null=True)
	home_phone_number = models.CharField(max_length = 32, verbose_name = 'شماره ثابت', null=True)
	address = models.CharField(max_length=256, verbose_name = 'آدرس', null=True, blank=True)
	price = models.IntegerField(verbose_name = 'قیمت', null=True)
	
	instant = models.DateTimeField(verbose_name="آگهی فوری", null=True, blank=True, default=timezone.now)
	is_stair = models.BooleanField(default=False, verbose_name="آگهی نردبان", null=True, blank=True)
	is_special = models.BooleanField(default=False, verbose_name="آگهی ویژه", null=True)
	expire_date = models.DateTimeField(verbose_name = 'زمان انقضا', default=timezone.now() + timezone.timedelta(days=30))
	priority = models.IntegerField(default=0, null=True, blank=True)
	
	status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="وضعیت",null=True)
	rent_type = models.CharField(max_length=1, choices=RENT_TYPE, null=True)
	
	favorite = models.ManyToManyField(User, related_name='favorite',verbose_name='مورد علاقه', blank=True)
	ratings = GenericRelation(Rating, verbose_name='امتیاز', related_query_name='object_list', null=True, blank=True)
	hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
	 	related_query_name='hit_count_generic_relation',)

	created_at = models.DateTimeField(auto_now_add = True, verbose_name = 'تاریخ ساخته شدن', null=True)
	updated_at = models.DateTimeField(auto_now = True, verbose_name = 'تاریخ آپدیت', null=True)

	class Meta:
		ordering = ['-created_at']
		verbose_name = 'آگهی'
		verbose_name_plural = 'آگهی ها'
	
	def __str__(self):
		return self.title
	
	def __repr__(self):
		return self.__str__()

	def get_absolute_url(self):
		return reverse('accounts:detail', kwargs={'pk': self.pk})
	
	def avaregereview(self):
		reviews = Comment.objects.filter(rent=self, active=True).aggregate(avarage=Avg('ratings'))
		avg = 0
		if reviews["avarage"] is not None:
			avg = float(reviews["avarage"])
		return avg

	def jpublish(self):
		return jalali_converter(self.created_at)
	jpublish.short_description = "زمان انتشار"

	def is_expired(self):
		if self.expire_date > timezone.now():
			return False
		else:
			return True
	is_expired.boolean = True
	is_expired.short_description = "وضعیت انقضای آگهی"

	def is_instant(self):
		if self.instant > timezone.now():
			return True
		else:
			return False
	is_instant.boolean = True
	is_instant.short_description = "وضعیت آگهی فوری"

	def days_until_expiration(self):
		date = (self.expire_date - datetime.timedelta(30))
		return date.day

	objects = RentManager()


class Category(MPTTModel):
	""" Model definition for Categories. """

	name = models.CharField(max_length=50, unique=True, verbose_name = 'نام دسته بندی')
	slug = models.SlugField(allow_unicode = True, verbose_name = 'آدرس دسته بندی', null=True)
	parent = TreeForeignKey('self', verbose_name = 'دسته بندی پدر', on_delete = models.CASCADE, null=True, blank=True, related_name='children', db_index=True)
	status = models.BooleanField(default=True, verbose_name="آیا نمایش داده شود؟")

	class MPTTMeta:
		order_insertion_by = ['name']
	
	class Meta:
		unique_together = (('parent', 'slug',))
		verbose_name = 'دسته بندی'
		verbose_name_plural = 'دسته بندی ها'

	def get_slug_list(self):
		try:
			ancestors = self.get_ancestors(include_self=True)
		except:
			ancestors = []
		else:
			ancestors = [ i.slug for i in ancestors]
		slugs = []
		for i in range(len(ancestors)):
			slugs.append('/'.join(ancestors[:i+1]))
		return slugs

	def __repr__(self):
		return self.name

	def __str__(self):
		return self.name

	objects = CategoryManager()


class State(models.Model):
	""" Model definition for States. """
	
	name = models.CharField(max_length=30, verbose_name = 'نام استان', null=True)

	class Meta:
		verbose_name = 'استان'
		verbose_name_plural = 'استان ها'
	
	def __str__(self):
		return self.name


class City(models.Model):
	""" Model definition for Cities. """
	state = models.ForeignKey(State, on_delete=models.CASCADE, verbose_name='استان')
	name = models.CharField(max_length=30, verbose_name = 'نام شهر')

	class Meta:
		verbose_name = 'شهر'
		verbose_name_plural = 'شهر ها'

	def __str__(self):
		return self.name


class Comment(models.Model):
	""" Model definition for Comments. """

	fullname = models.CharField(verbose_name='نام و نام خانوادگی', max_length=50, null=True)
	comment_text = models.TextField(verbose_name='متن دیدگاه', null=True)
	ip = models.CharField(max_length=20, blank=True, verbose_name='آدرس ای پی', null=True)
	
	ratings = models.IntegerField(default=0, verbose_name='امتیاز', null=True)
	
	rent = models.ForeignKey(Rent, on_delete=models.CASCADE, null=True, related_name='comments')
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر', null=True)
	
	active = models.BooleanField(default=False, verbose_name='وضعیت دیدگاه', null=True)
	
	created_at = models.DateTimeField(auto_now_add=True, verbose_name= 'تاریخ ساخته شدن', null=True)

	class Meta:
		ordering = ['-created_at']
		verbose_name = 'نظر'
		verbose_name_plural = 'نظرات'

	def __str__(self):
		return 'Comment {} by {}'.format(self.comment_text, self.fullname)

	objects = CommentManager()


class Images(models.Model):
	""" Model definition for Images. """

	file = models.FileField(null=True, blank=True, upload_to='uploads/ads-images/%Y-%m-%d/', verbose_name = 'تصویر')
	rent = models.ForeignKey(Rent, related_name='images', null=True, on_delete = models.CASCADE)

	class Meta:
		verbose_name = 'تصویر'
		verbose_name_plural = 'تصاویر'














