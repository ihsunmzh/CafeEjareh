from django.contrib import admin
from django.urls import path, re_path, include
from mysite import views

app_name = 'mysite'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about-us/', views.AboutUsView.as_view(), name='about'),
    path('page-contact/', views.ContactUsView.as_view(), name='page-contact'),
    path('page-how-it-work/', views.HowItWorkView.as_view(), name='page-how-it-work'),
    path('page-policy/', views.PolicyView.as_view(), name='page-policy'),
    path('page-faq/', views.QuestionsView.as_view(), name='page-faq'),
    path('search/', views.SearchView.as_view(), name='search'),
]
