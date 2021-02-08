from django.db import models

from accounts.models import User
from rent.models import Rent


class Order(models.Model):
	""" Model definition for Payments. """
	
	STATUS_CHOICES = (
	 ('P', 'payment'),
	 ('U', 'unpaid'),
	)   

	order_id = models.AutoField(primary_key = True)
	owner = models.ForeignKey(User, on_delete = models.CASCADE,verbose_name='کاربری سفارش', null=True)
	rent = models.ForeignKey(Rent, on_delete = models.CASCADE,verbose_name=' آگهی', null=True)
	type_order = models.CharField(max_length=100 ,null = True , blank = True , verbose_name = 'نوع سفارش')
	status = models.CharField(max_length=20, choices=STATUS_CHOICES ,default='unpaid', verbose_name = 'وضعیت سفارش')
	refid = models.IntegerField(default=0, null = True , blank = True , verbose_name = 'شماره پیگیری تراکنش')
	total = models.IntegerField(default=0, null = True , blank = True , verbose_name = ' مبلغ سفارش')
	statuscode = models.IntegerField( null = True , blank = True , verbose_name = 'کد وضعیت')

	class Meta:
		verbose_name = 'سفارش'
		verbose_name_plural = 'سفارشات'

	def __str__(self):
	 return  str(self.order_id) + "   " + str(self.owner)+ "   " + str(self.status)+ "   " + str(self.rent)    