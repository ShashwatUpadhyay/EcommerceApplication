from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop , name='shop'),
    path('<slug>/', views.product_page , name='product')
]
