from django.urls import path

from . import views
urlpatterns = [
    path('address-edit/<uid>/', views.address_edit, name='address_edit'),
    path('add-address/', views.add_address, name='add_address'),
    path('delete-address/<uid>/', views.delete_address, name='delete_address'),
    path('password-reset-form', views.ForgetPassword, name='password_reset'),
    path('password-reset-confirm/<token>', views.change_password, name='password_reset_confirm'),
    
    
]
