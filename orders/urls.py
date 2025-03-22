from django.urls import path
from . import views

urlpatterns = [
    path('', views.order , name='order'),
    path('add-to-cart/', views.addToCart , name='addToCart'),
    path('remove-from-cart/', views.removeFromCart , name='removeFromCart'),
    path('remove-item/', views.removeItem , name='removeItem'),
    path('cart/', views.cart , name='cart'),
    path('cart/shipping/', views.shipping , name='shipping'),
    path('cart/shipping/payment/', views.payment , name='payment'),
]
