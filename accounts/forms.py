from django import forms
from django.forms import ClearableFileInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts.models import User
from rent.models import (
	Rent,
	Category,
	City,
	Comment,
	Images
)
from mptt.fields import TreeNodeChoiceField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _   


class ProfileForm(forms.ModelForm):
	avatar = forms.ImageField(required=False)

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user')

		super(ProfileForm, self).__init__(*args, **kwargs)

		self.fields['sex'].widget.attrs\
			.update({
				'class': 'el-select2-set-gender'
			})

		if not user.is_superuser:
			self.fields['email'].disabled = True

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'mobile_number', 'home_phone_number', 'sex',
					'avatar', 'email', 'bio']
		

class SignupForm(UserCreationForm):
	email = forms.EmailField(max_length=200)
	username = forms.CharField(max_length=64)
	accept_policy = forms.BooleanField(required=True)

	class Meta:
		model = User
		fields = ('email', 'username', 'mobile_number', 'password1', 'password2', 'accept_policy')


class LoginForm(AuthenticationForm):
	username = forms.CharField(label='Email / Username')
	remember_me = forms.BooleanField(required=False)


class ImagesForm(forms.ModelForm):

	class Meta:
		model = Images
		fields = ('file',)
		widgets = {
			'file': ClearableFileInput(attrs={'multiple': True}),
		}


class CreateRentForm(forms.ModelForm):
	category = TreeNodeChoiceField(queryset=Category.objects.all())
	image = forms.ImageField(widget=forms.FileInput(attrs={'multiple': True}), required=False)

	class Meta:
		model = Rent
		fields = ('category', 'price', 'mobile_number', 'home_phone_number', 'image',
					'rent_type', 'state', 'city', 'address', 'title', 'description')
		widgets = {
			'description': forms.Textarea(attrs={'rows':10, 'cols':30}),
		}

	def __init__(self, *args, **kwargs):
		super(CreateRentForm, self).__init__(*args, **kwargs)
		self.fields['home_phone_number'].required = False

		# Get Cities Of Current State
		self.fields['city'].queryset = City.objects.none()

		if 'state' in self.data:
			try:
				state_id = int(self.data.get('state'))
				self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('name')
			except (ValueError, TypeError):
				pass  # invalid input from the client; ignore and fallback to empty City queryset
		elif self.instance.pk:
			self.fields['city'].queryset = self.instance.state.city_set.order_by('name')
			
		self.fields['category'].widget.attrs\
			.update({
				'class': 'el-select2-set-category'
			})

		self.fields['rent_type'].widget.attrs\
			.update({
				'class': 'el-select2-set-date'
			})

		self.fields['state'].widget.attrs\
			.update({
				'class': 'el-select2-set-date'
			})

		self.fields['city'].widget.attrs\
			.update({
				'class': 'el-select2-set-date'
			})

		self.fields['description'].widget.attrs['rows'] = 10
		self.fields['description'].widget.attrs['columns'] = 30

	def clean_mobile_number(self):
		mobile_number = self.cleaned_data.get('mobile_number')

		except_values = ['<', '>', '/']

		for e_v in except_values:

			if e_v in mobile_number:

				raise ValidationError(
					_('You can not use `<, >, /`'),
					code = _('forbidden')
				)

		return mobile_number

	def clean_title(self):
		title = self.cleaned_data.get('title')

		except_values = ['<', '>', '/']

		for e_v in except_values:

			if e_v in title:

				raise ValidationError(
					_('You can not use `<, >, /`'),
					code = _('forbidden')
				)

		return title

	def clean_description(self):
		description = self.cleaned_data.get('description')

		except_values = ['<', '>', '/']

		for e_v in except_values:

			if e_v in description:

				raise ValidationError(
					_('You can not use `<, >, /`'),
					code = _('forbidden')
				)

		return description

	def clean(self):
		cleaned_data = super(CreateRentForm, self).clean()

		title = cleaned_data.get('title')
		description = cleaned_data.get('description')
		category = cleaned_data.get('category')
		state = cleaned_data.get('state')
		city = cleaned_data.get('city')
		mobile_number = cleaned_data.get('mobile_number')
		address = cleaned_data.get('address')
		price = cleaned_data.get('price')

		if not title:
			raise ValidationError(
				_('لطفا عنوان را کنید ..'),
				code = _('forbidden')
			)

		if not description:
			raise ValidationError(
				_('لطفا توضیحات را وارد کنید ..'),
				code = _('forbidden')
			)

		if not category:
			raise ValidationError(
				_('لطفا دسته بندی را انتخاب کنید ..'),
				code = _('forbidden')
			)

		if not state:
			raise ValidationError(
				_('لطفا استان خود را وارد کنید ..'),
				code = _('forbidden')
			)

		if not city:
			raise ValidationError(
				_('لطفا شهر خود را وارد کنید ..'),
				code = _('forbidden')
			)

		if not mobile_number:
			raise ValidationError(
				_('لطفا شماره موبایل را وارد کنید ..'),
				code = _('forbidden')
			)

		if not address:
			raise ValidationError(
				_('لطفا آدرس را وارد کنید ..'),
				code = _('forbidden')
			)

		if not price:
			raise ValidationError(
				_('لطفا قیمت را وارد کنید ..'),
				code = _('forbidden')
			)


class CommentForm(forms.ModelForm):

	class Meta:
		model = Comment
		fields = ('fullname', 'comment_text', 'ratings',)

	def clean_fullname(self):
		fullname = self.cleaned_data.get('fullname')

		except_values = ['<', '>', '/']

		for e_v in except_values:

			if e_v in fullname:

				raise ValidationError(
					_('You can not use `<, >, /`'),
					code = _('forbidden')
				)

		return fullname

	def clean_comment_text(self):
		comment_text = self.cleaned_data.get('comment_text')

		except_values = ['<', '>', '/']

		for e_v in except_values:

			if e_v in comment_text:

				raise ValidationError(
					_('You can not use `<, >, /`'),
					code = _('forbidden')
				)

		return comment_text

	def clean(self):
		cleaned_data = super(CommentForm, self).clean()

		fullname = cleaned_data.get('fullname')
		comment_text = cleaned_data.get('comment_text')

		if not fullname:
			raise ValidationError(
				_('لطفا این فیلد را پر کنید ..'),
				code = _('forbidden')
			)

		if not comment_text:
			raise ValidationError(
				_('لطفا این فیلد را پر کنید ..'),
				code = _('forbidden')
			)