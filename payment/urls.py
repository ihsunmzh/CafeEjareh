from django.urls import path
from payment import views
from django.conf.urls import url
from django.conf import settings

app_name = 'payment'

urlpatterns = [
    path('<int:item_id>-<str:item_type>/', views.request, name='request'),
    path('verify', views.verify, name='verify'),
]