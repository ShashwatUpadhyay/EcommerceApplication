from django.urls import path
from . import views

urlpatterns = [
    path('', views.order , name='order'),
    path('add-to-cart/', views.addToCart , name='addToCart'),
]
