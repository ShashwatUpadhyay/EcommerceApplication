from django.urls import path
from . import views

urlpatterns = [
    # path('payment/', views.payment , name='payment'),
    path('', views.my_orders , name='my_orders'),
    path('cart/', views.cart , name='cart'),
    path('cart_/', views.cart_ , name='cart_'),
    path('order-processing/', views.my_orders_ordersprocessing , name='orders_processing'),
    path('order-shipped/', views.my_orders_ordershipped , name='orders_shipped'),
    path('order-delivered/', views.my_orders_orderdelivered , name='orders_delivered'),
    path('order-canceled/', views.my_orders_ordercanceled , name='order_canceled'),
    path('order/<uid>/', views.order , name='order'),

    path('add-to-cart/', views.addToCart , name='addToCart'),
    path('remove-from-cart/', views.removeFromCart , name='removeFromCart'),
    path('remove-item/', views.removeItem , name='removeItem'),
    path('shipping/', views.shipping , name='shipping'),
    path('shipping_/', views.shipping_ , name='shipping_'),
    path("select-address/", views.select_address, name="select_address"),
    path("place-order/", views.order_place, name="order_place"),
    path("order-place_/", views.order_place_, name="order_place_"),
    path("payment/", views.payment, name="payment"),
    path("payment_/", views.payment_, name="payment_"),
    path("paymenthandler/<uid>/", views.paymenthandler, name="paymenthandler"),
    path("paymenthandler_/<uid>/", views.paymenthandler_, name="paymenthandler_"),
    
    path('add_to_cart/<customer_uid>/<product_uid>/', views.addToCartAPI, name='addToCartAPI'),
    path('remove_from_cart/<customer_uid>/<product_uid>/', views.removeFromCartAPI, name='removeFromCartAPI'),
    path('add_to_cart_n/<product_uid>/', views.add_to_cart_of_unauthenticated, name='add_to_cart_of_unauthenticated'),
    path('remove_from_cart_n/<product_uid>/', views.remove_from_cart_of_unauthenticated, name='remove_from_cart_of_unauthenticated'),
    path('remove_item_cart_n/<product_uid>/', views.remove_item_of_unauthenticated, name='remove_item_of_unauthenticated'),
    
    # admin view
    path('a/orders/', views.AllOrders, name='AllOrders'),
    path('a/pending-orders/', views.PendingOrders, name='PendingOrders'),
    path('a/processing-orders/', views.ProcessingOrders, name='ProcessingOrders'),
    path('a/shipped-orders/', views.ShippedOrders, name='ShippedOrders'),
    path('a/delevered-orders/', views.DeleveredOrders, name='DeleveredOrders'),
    path('a/canceled-orders/', views.CanceledOrders, name='CanceledOrders'),
    path('a/mark-as-shipped/<order_uid>/', views.markAsShiped, name='markAsShiped'),
    path('a/mark-as-canceled/<order_uid>/', views.markAsCanceled, name='markAsCanceled'),
    path('a/mark-as-delivered/<order_uid>/', views.markAsDelivered, name='markAsDelivered'),
    path('a/mark-as-processing/<order_uid>/', views.markAsProcessing, name='markAsProcessing'),
    path('a/low-stock', views.low_stock, name='low_stock'),
    path('order_confirmation/<order_uid>', views.order_confirmation, name='order_confirmation'),
    path('download-invoice/<order_uid>', views.download_invoice, name='download_invoice'),
]
