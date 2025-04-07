from django.urls import path
from . import views
from account.views import register,login_page,logoutpage
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_page, name='login'),
    path('logout/', logoutpage, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('track/', views.track, name='track'),
    path('track/<number>/', views.track_order, name='track_order'),
]
