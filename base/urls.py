from django.urls import path
from . import views
from account.views import register,login_page
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_page, name='login'),
]
