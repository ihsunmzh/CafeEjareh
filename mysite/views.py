from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.contrib.messages.views import SuccessMessageMixin

from django.views.generic import CreateView, ListView, TemplateView
from django.views.generic.edit import FormMixin

from django.urls import reverse_lazy 

from rent.models import Rent, Category
from mysite.models import Contact

from mysite.forms import ContactForm, SearchForm

from datetime import datetime, timedelta


class IndexView(TemplateView):
	template_name = 'mysite/index.html'

	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		context['latest_ads'] = Rent.objects.published().order_by('-created_at')[:6]
		context['hit_ads'] = Rent.objects.published().order_by('-hit_count_generic__hits')[:6]
		context['ads_number'] = Rent.objects.published().count()
		return context
	

class AboutUsView(TemplateView):
	template_name = 'mysite/page-about.html'


class ContactUsView(SuccessMessageMixin, CreateView):
	template_name = 'mysite/page-contact.html'
	model = Contact
	form_class = ContactForm
	success_url = reverse_lazy('mysite:page-contact')
	success_message = "پیام شما با موفقیت ارسال شد. در اولین فرصت پاسخگو هستیم!"


class HowItWorkView(TemplateView):
	template_name = 'mysite/page-how-it-works.html'


class PolicyView(TemplateView):
	template_name = 'mysite/page-policy.html'


class QuestionsView(TemplateView):
	template_name = 'mysite/page-faq.html'


class SearchView(FormMixin, ListView):
	template_name = 'mysite/search.html'
	model = Rent
	form_class = SearchForm
	paginate_by = 12
	
	def get_queryset(self):
		object_list = Rent.objects.published().order_by('-created_at', 'priority')

		title = self.request.GET.get('title', None)
		category = self.request.GET.get('category', None)
		city = self.request.GET.get('city', None)
		published_time = self.request.GET.get('published_time', None)
		is_have_image = self.request.GET.get('is_have_image', None)
		
		if title:
			object_list = object_list.filter(title__icontains = title)

		if category:
			object_list = object_list.filter(category = category)

		if city:
			object_list = object_list.filter(city = city)

		if is_have_image:
			object_list = object_list.filter(images__isnull=False)

		# Sort Items By Created Times -->
		if published_time:
			# my_date = datetime.now()

			# Order by daily --> 
			if published_time == "1D":
				last_day = datetime.today() - timedelta(days=1)
				object_list = object_list.filter(created_at__lte=last_day)

			if published_time == "2D":
				two_days_ago = datetime.today() - timedelta(days=2)
				object_list = object_list.filter(created_at__lte=two_days_ago)

			if published_time == "3D":
				twree_days_ago = datetime.today() - timedelta(days=3)
				object_list = object_list.filter(created_at__lte=twree_days_ago)

			# Order by weekly -->
			if published_time == "1W":
				one_week_ago = datetime.today() - timedelta(days=7)
				object_list = object_list.filter(created_at__lte=one_week_ago)

			if published_time == "2W":
				two_weeks_ago = datetime.today() - timedelta(days=14)
				object_list = object_list.filter(created_at__lte=two_weeks_ago)

			if published_time == "3W":
				twree_weeks_ago = datetime.today() - timedelta(days=21)
				object_list = object_list.filter(created_at__lte=twree_weeks_ago)

			# Order by monthly --> 
			if published_time == "1M":
				last_month = datetime.today() - timedelta(days=30)
				object_list = object_list.filter(created_at__lte=last_month)

			if published_time == "2M":
				two_months_ago = datetime.today() - timedelta(days=60)
				object_list = object_list.filter(created_at__lte=two_months_ago)

			if published_time == "3M":
				three_months_ago = datetime.today() - timedelta(days=90)
				object_list = object_list.filter(created_at__lte=three_months_ago)

		return object_list