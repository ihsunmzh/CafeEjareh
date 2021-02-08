from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.messages.views import SuccessMessageMixin

from django.http import HttpResponseRedirect, JsonResponse, HttpResponse

from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404, render, render_to_response

from django.urls import reverse_lazy, reverse

from django.views.generic import CreateView, DetailView, DeleteView, FormView, ListView, TemplateView, UpdateView, View
from django.views.generic.edit import ModelFormMixin, FormMixin

from accounts.forms import CreateRentForm, CommentForm, ImagesForm, SignupForm, ProfileForm, LoginForm

from accounts.models import User
from rent.models import Comment, Category, City, Images, Rent

from painless.mixins import AuthorAccessMixin, AuthorsAccessMixin, FormValidMixin, SuperUserAccessMixin


class Register(CreateView):
	form_class = SignupForm
	template_name = "registration/sign-up.html"
	success_url = reverse_lazy('accounts:home')

	def form_valid(self, form):
		user = form.save(commit=False)
		user.is_active = True
		user.is_author = True
		user.save()
		username = form.cleaned_data.get('username')
		raw_password = form.cleaned_data.get('password1')

		user = authenticate(username = username, password = raw_password)
		
		login(self.request, user)
		return redirect(self.success_url)


class Login(LoginView):
	template_name = 'registration/sign-in.html'
	form_class = LoginForm
	success_url = reverse_lazy('accounts:home')

	def form_valid(self, form):
		remember_me = form.cleaned_data['remember_me']

		if not remember_me:
			self.request.session.set_expiry(0)
			self.request.session.modified = True
		return super(Login, self).form_valid(form)


class Profile(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
	model = User
	template_name = "dashboard/profile.html"
	form_class = ProfileForm
	success_url = reverse_lazy("accounts:home")
	success_message = 'کاربر گرامی تغییرات پروفایل شما با موفقیت ثبت شد.'

	def get_object(self):
		return User.objects.get(pk = self.request.user.pk)

	def get_form_kwargs(self):
		kwargs = super(Profile, self).get_form_kwargs()
		kwargs.update({
			'user': self.request.user
		})
		return kwargs


class Home(TemplateView):
	template_name = "dashboard/index.html"

	def get_context_data(self, **kwargs):
		context = super(Home, self).get_context_data(**kwargs)
		context['users_posts_count'] = Rent.objects.filter(author=self.request.user).count()
		context['users_special_posts_count'] = Rent.objects.filter(author=self.request.user, is_special=True).count()
		context['date_joined'] = self.request.user.date_joined
		return context
	

class RentList(ListView):
	template_name = "dashboard/my-ads.html"
	context_object_name = 'list'

	def get_queryset(self):
		if self.request.user.is_superuser:
			return Rent.objects.all()
		else:
			return Rent.objects.filter(author=self.request.user)


class RentPreview(AuthorAccessMixin, DetailView):
	template_name = 'dashboard/product.html'
	context_object_name = 'product'

	def get_object(self):
		pk = self.kwargs.get('pk')
		return get_object_or_404(Rent, pk=pk)
	
	
def load_cities(request):
	state_id = request.GET['state']
	cities = City.objects.filter(state__id=state_id).order_by('name')
	return render(request, 'hr/city_dropdown_list_options.html', {'cities': cities})


class RentCreate(SuccessMessageMixin, LoginRequiredMixin, View):
	model = Rent
	form_class = CreateRentForm
	success_url = reverse_lazy('accounts:home')
	template_name = "dashboard/create.html"

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST, request.FILES)
		if form.is_valid():
			form = form.save(commit=False)
			form.author = self.request.user
			form.status = 'i'
			form.save()
			rent=form
			if self.request.FILES:
				for i in self.request.FILES.getlist('image'):
					Images.objects.create(rent=rent,file=i)
			messages.success(request, 'کاربر گرامی آگهی شما بعد از تایید ناظر طی ۸ ساعت آینده منتشر میگردد.')
			return redirect(self.success_url)
		else:
			return render(request, self.template_name, {'form': form})


class RentUpdate(LoginRequiredMixin,AuthorAccessMixin, UpdateView):
	model = Rent
	template_name = "dashboard/update.html"
	form_class = CreateRentForm
	success_url = reverse_lazy('accounts:home')


class RentDelete(DeleteView):
	model = Rent
	success_url = reverse_lazy('accounts:home')
	template_name = "dashboard/rent_confirm_delete.html"

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		if self.object.author == request.user:
			self.object.delete()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return HttpResponse('404_url')


class AddToFavorite(UpdateView):
	http_method_names = ['post', 'get',]
	model = Rent

	def get(self, *args, **kwargs):
		self.object = self.get_object()

		if self.object.favorite.filter(id=self.request.user.id).exists():
			self.object.favorite.remove(self.request.user)
		else:
			self.object.favorite.add(self.request.user)

		return redirect('accounts:detail', pk=self.object.pk)


class FavoritesList(ListView):
	template_name = 'dashboard/favorites.html'
	model = Rent

	def get_queryset(self):
		queryset = super(FavoritesList, self).get_queryset()
		global user
		user = self.request.user
		queryset = user.favorite.all()
		return queryset
	
	def get_context_data(self, **kwargs):
		context = super(FavoritesList, self).get_context_data(**kwargs)
		context['favorites_list'] = user.favorite.all()

		return context
	

class RentDetailView(FormMixin, DetailView):
	template_name = 'mysite/product.html'
	form_class = CommentForm

	def get_object(self):
		pk = self.kwargs.get('pk')
		return get_object_or_404(Rent.objects.published(), pk=pk)

	def get_success_url(self):
		return reverse('accounts:detail', kwargs={'pk': self.object.pk})

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form = CommentForm(request.POST or None)
		if form.is_valid():
			form.instance.rent = Rent.objects.get(pk=self.object.pk)
			form.save()
			return self.form_valid(form)
		else:
			return self.form_invalid(form)