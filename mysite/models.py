from django.db import models


class Contact(models.Model):
	""" Model definition for Contacts. """

	full_name = models.CharField(max_length=50, verbose_name='نام کامل', null=True)
	email = models.EmailField(max_length=254, verbose_name='ایمیل',  null=True)
	text = models.TextField(verbose_name='متن', null=True)
	created_at = models.DateTimeField(auto_now_add = True, verbose_name = 'تاریخ ساخته شدن', null=True)

	def __str__(self):
		return self.full_name

	def __repr__(self):
		return self.__str__()

	class Meta:
		ordering = ('-created_at',)
		verbose_name = 'تماس با ما'
		verbose_name_plural = 'تماس با ما'