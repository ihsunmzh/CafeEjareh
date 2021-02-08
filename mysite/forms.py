from django import forms
from rent.models import Rent, Comment, Category, City
from mysite.models import Contact
from mptt.fields import TreeNodeChoiceField 


class SearchForm(forms.ModelForm):
	title = forms.CharField(max_length=128, required=False)
	category = TreeNodeChoiceField(queryset=Category.objects.all(), required=False)

	# Published At Choices -->
	PUBLISHED_TIME_CHOICES = (
		('', 'جست و جو بر اساس تاریخ آگهی'),

		('روزانه', (
				('1D', 'یک روز پیش'),
				('2D', 'دو روز پیش'),
				('3D', 'سه روز پیش'),
			)
		),

		('هفتگی', (
				('1W', 'یک هفته پیش'),
				('2W', 'دو هفته پیش'),
				('3W', 'سه هفته پیش'),
			)
		),
		('ماهیانه', (
				('1M', 'یک ماه پیش'),
				('2M', 'دو ماه پیش'),
				('3M', 'سه ماه پیش'),
			)
		),
	)

	published_time = forms.ChoiceField(
		choices=PUBLISHED_TIME_CHOICES
	)
	is_have_image = forms.BooleanField(required=False)

	# My Custom Styles -->
	title.widget.attrs.update({"class": "form-item", "placeholder": "جست و جو بر اساس نام کالا"})
	category.widget.attrs.update({"class": "el-select2-category"})

	class Meta:
		model = Rent
		fields = ('title', 'category', 'city', 'published_time', 'is_have_image')

	def __init__(self, *args, **kwargs):
		super(SearchForm, self).__init__(*args, **kwargs)
		self.fields['city'].widget.attrs\
			.update({
				'class': 'el-select2-city'
			})
		self.fields['published_time'].widget.attrs\
			.update({
				'class': 'el-select2-date'
			})
		self.fields['title'].required = False
		self.fields['category'].required = False
		self.fields['city'].required = False
		self.fields['published_time'].required = False
		self.fields['is_have_image'].required = False


class ContactForm(forms.ModelForm):

	class Meta:
		model = Contact
		fields = ('full_name', 'email','text',)






