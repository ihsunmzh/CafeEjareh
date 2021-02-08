from django.db import models


# Category Manager -->
class CategoryManager(models.Manager):
	def active(self):
		return self.filter(status=True)


# Article Manager -->
class ArticleManager(models.Manager):
	def published(self):
		return self.filter(status='p')