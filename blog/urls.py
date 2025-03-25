from django.urls import path
from . import views


urlpatterns = [
    path('', views.post_page , name='blog_page'),
    path('Blog-post/<slug>', views.blog , name='blog'),
]
