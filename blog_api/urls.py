from django.urls import path
from blog_api.views import *
from rest_framework.authtoken import views

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('login/', views.obtain_auth_token),
    path('', test_api, name='test_api'),
    path('blogs', blogs_api, name='blogs_api'),
    path('categories', categories_api, name='categories_api'),
    path('my_blogs', MyBlogView.as_view()),
    path('post_blog', MyBlogView.as_view()),
    path('update_blog', UpdateBlogView.as_view()),
    path('delete_blog', MyBlogView.as_view()),
    path('register/', RegisterUserView.as_view()),
]
