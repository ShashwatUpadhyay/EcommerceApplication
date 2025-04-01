from django.urls import path
from . import views

urlpatterns = [
    path('wishlist/', views.wishlist , name='wishlist'),
    path('add-to-wishlist/<uid>', views.add_to_wishlist , name='add_to_wishlist'),
    path('remove-from-wishlist/<uid>', views.remove_wishlist , name='remove_wishlist'),
    path('', views.shop , name='shop'),
    path('image/<uid>/', views.get_img , name='image'),
    path('search/', views.search_suggestions , name='search'),
    path('<slug>/', views.product_page , name='product'),
    path('a/warehouse/', views.stockManage , name='stockManage'),
    path('a/warehouse/<uid>/', views.productEdit , name='productEdit'),
    
]
