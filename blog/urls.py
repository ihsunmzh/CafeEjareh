from django.urls import path, re_path
from blog import views


app_name = 'weblog'

urlpatterns = [
	path('<int:pk>', views.ArticleDetailView.as_view(), name="detail"),
    path('', views.ArticleView.as_view(), name = 'articles'),
]