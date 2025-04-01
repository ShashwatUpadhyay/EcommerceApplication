from django.urls import path
from . import views
urlpatterns = [
    path('Contact-us/', views.ContactUs, name='contact'),
]
