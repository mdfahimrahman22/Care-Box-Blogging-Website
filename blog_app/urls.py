from django.urls import path
from blog_app import views

urlpatterns = [
    path('', views.home, name='index'),
    path('home', views.home, name='home'),
]
