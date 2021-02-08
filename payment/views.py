from django.conf import settings

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect

from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.shortcuts import redirect, render

from django.utils import timezone

from payment.models import Order
from rent.models import Rent

from zeep import Client

from kernel.settings.secure import MERCHANT

client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')


@login_required
def request(request, item_id, item_type, phone='09123456789', email='mail@example.com', description='خرید از رنت کالا'):
	""" price per toman """
	phone = request.GET.get('phone') if phone else phone
	email = request.user.email
	description = 'خرید از رنت کالا'

	if item_type not in ['آگهی فوری', 'آگهی نردبان', 'آگهی فوری و نردبان']:
		messages.error(request, 'اوه! یه مشکلی پیش اومده...')
		return HttpResponseRedirect('/')

	if item_type == 'آگهی فوری':
		total = 12000
	elif item_type == 'آگهی نردبان':
		total = 8000
	elif item_type == 'آگهی فوری و نردبان':
		total = 15000

	if Order.objects.filter(status = 'unpaid'):
		Order.objects.get(status='unpaid').delete() 
	
	rent = Rent.objects.get(id=item_id)	
	order = Order(owner=request.user , rent=rent , type_order = item_type , total=total ).save()	
	
	CallbackURL  = 'http://127.0.0.1:8000/payment/verify'
	result = client.service.PaymentRequest(MERCHANT, total , description, email, phone, CallbackURL)

	if result.Status == 100:
		return redirect('https://sandbox.zarinpal.com/pg/StartPay/' + str(result.Authority))
	else :
		return HttpResponse('Error code: ' + str(result.Status))	


def verify(request):
	
	if request.GET.get('Status') == 'OK':

		order = Order.objects.get(status='unpaid')
		rent = Rent.objects.get(id=order.rent.id)
		total = order.total

		result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], total)

		if result.Status == 100 or result.Status == 101  :

			order.refid = result.RefID
			order.statuscode = result.Status
			order.status = 'payment'
			order.save()

			if order.type_order == 'آگهی فوری' :
				rent.instant = timezone.now() + timezone.timedelta(days=7)
				rent.is_special = True
				rent.save()
				return HttpResponse("کاربر گرامی درخواست شما با موفقیت ثبت گردید.")

			elif order.type_order == 'آگهی نردبان' :
				rent.is_stair = True
				rent.priority = 1000
				rent.is_special = True
				rent.save()
				return HttpResponse("کاربر گرامی درخواست شما با موفقیت ثبت گردید.")

			elif order.type_order == 'آگهی فوری و نردبان' :
				rent.instant = timezone.now() + timezone.timedelta(days=7)
				rent.is_stair = True
				rent.priority = 1000
				rent.is_special = True
				rent.save()
				return HttpResponse("کاربر گرامی درخواست شما با موفقیت ثبت گردید.")

		else :
			order.statuscode = result.Status
			order.save()
			return HttpResponse ('خطا')

	else :
		return HttpResponse("خطا")