
from django.urls import path
from .views import *
from . import views
urlpatterns = [
path('',homepage,name='home'),
path('register',register,name='register'),
path('login',loginview,name='login'),
path('logout',LogoutPage,name='logout'),
path('blog_single/<int:id>', blog_single, name='blog_single'),
path('post_comment/', post_comment, name='post_comment'),
path('contact',contact,name='contact'),
path('edit_profile/', views.edit_profile, name='edit_profile'),

path('about',about,name='about'),
path('profile/', views.profile, name='profile'),
path('category/<str:category_name>/', views.category_view, name='category_view'),
path('search/', views.search_view, name='search'),

]