from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_orders , name='my_orders'),
    path('cart/', views.cart , name='cart'),
    path('order-processing/', views.my_orders_ordersprocessing , name='orders_processing'),
    path('order-shipped/', views.my_orders_ordershipped , name='orders_shipped'),
    path('order-delivered/', views.my_orders_orderdelivered , name='orders_delivered'),
    path('order-canceled/', views.my_orders_ordercanceled , name='order_canceled'),
    path('order/<uid>/', views.order , name='order'),

    path('add-to-cart/', views.addToCart , name='addToCart'),
    path('remove-from-cart/', views.removeFromCart , name='removeFromCart'),
    path('remove-item/', views.removeItem , name='removeItem'),
    path('shipping/', views.shipping , name='shipping'),
    path('payment/', views.payment , name='payment'),
    path("select-address/", views.select_address, name="select_address"),
    path("place-order/", views.order_place, name="order_place"),

]
