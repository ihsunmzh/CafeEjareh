from django.db import models


# Rent Manager
class RentManager(models.Manager):
	def published(self):
		return self.filter(status='p')


# Category Manager
class CategoryManager(models.Manager):
	def active(self):
		return self.filter(status = True)


# Comment Manager
class CommentManager(models.Manager):
	def active(self):
		return self.filter(active=True)