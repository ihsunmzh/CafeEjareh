from django.contrib import admin
from payment.models import *
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id','status','owner','rent')
    ordering = ('order_id',)	


admin.site.register(Order,OrderAdmin)	    

