from django.contrib.auth import views
from django.urls import path, re_path
from .views import (
	RentList,
	RentDetailView,
	RentCreate,
	RentUpdate,
	RentDelete,
	AddToFavorite,
	Profile,
	Home,
	RentPreview,
	FavoritesList,
	load_cities,
)

app_name = 'accounts'

urlpatterns = [
	path('', Home.as_view(), name="home"),
	path('ads/<int:pk>', RentDetailView.as_view(), name="detail"),
	path('my-ads/', RentList.as_view(), name="my-ads"),
	path('rent-create', RentCreate.as_view(), name="rent-create"),
	path('preview/<int:pk>', RentPreview.as_view(), name="rent-preview"),
	path('rent-update/<int:pk>', RentUpdate.as_view(), name="rent-update"),
	path('rent-delete/<int:pk>', RentDelete.as_view(), name="rent-delete"),
	path('my-favorites/', FavoritesList.as_view(), name="my-favorites"),
	path('<int:pk>/rent-favorite/', AddToFavorite.as_view(), name="rent-favorite"),
	path('profile/', Profile.as_view(), name="profile"),
	path('ajax/load-cities/', load_cities, name='ajax_load_cities'),
]