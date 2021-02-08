from django.db import models

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from django.utils.html import format_html
from django.utils.text import slugify

from django.urls import reverse

from accounts.models import User
from mptt.models import MPTTModel
from mptt.models import TreeForeignKey

from .managers import ArticleManager, CategoryManager


class Article(models.Model):
	""" Model definition for Articles. """

	STATUS_CHOICES = (
		('d', 'پیش‌نویس'),
		('p', 'منتشر شده'),
	)

	title = models.CharField(max_length=200, verbose_name="عنوان مقاله")
	slug = models.SlugField(max_length=100, allow_unicode=True, unique=True, verbose_name="آدرس مقاله")
	description = RichTextUploadingField(verbose_name="محتوا")
	
	author = models.ForeignKey(User, null=True, on_delete=models.CASCADE, verbose_name="نویسنده")
	category = TreeForeignKey('Category', verbose_name="دسته‌بندی", on_delete=models.CASCADE, null=True)
	thumbnail = models.ImageField(upload_to="site/blog", verbose_name="تصویر مقاله")
	status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="وضعیت")
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "مقاله"
		verbose_name_plural = "مقالات"
		ordering = ['-created_at']

	def __str__(self):
		return self.title

	def __repr__(self):
		return self.__str__()

	def thumbnail_tag(self):
		return format_html("<img width=100 height=75 style='border-radius: 5px;' src='{}'>".format(self.thumbnail.url))
	thumbnail_tag.short_description = "عکس"	

	objects = ArticleManager()


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

	def __str__(self):
		return self.name

	def __repr__(self):
		return self.__str__()

	objects = CategoryManager()