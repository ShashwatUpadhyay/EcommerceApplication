from django.urls import path
from . import views
from account.views import register,login_page,logoutpage
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_page, name='login'),
    path('logout/', logoutpage, name='logout'),
    path('profile/', views.profile, name='profile'),
]
