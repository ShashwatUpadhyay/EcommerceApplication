from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop , name='shop'),
    path('image/<uid>/', views.get_img , name='image'),
    path('search/', views.search_suggestions , name='search'),
    path('<slug>/', views.product_page , name='product'),
    path('a/warehouse/', views.stockManage , name='stockManage'),
    path('a/warehouse/<uid>/', views.productEdit , name='productEdit'),
]
