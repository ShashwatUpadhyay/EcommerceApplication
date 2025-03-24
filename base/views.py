from django.shortcuts import render
from shop.models import *
from itertools import groupby
from operator import attrgetter
from math import ceil
from account.models import UserExtra
from django.contrib.auth.decorators import login_required
# Create your views here.
 
def home(request):
    categories = ProductCategory.objects.all()
    products = [category.products.first() for category in categories if category.products.exists()]
    
    slides = [products[i:i+4] for i in range(0, len(products), 4)]
    cat = ProductCategory.objects.all().distinct()
    context = {
        'products':products,
        'catogery':cat,
        'slides': slides
    }
    return render(request,'home.html',context)

@login_required(login_url='login')
def profile(request):
    user = request.user
    user = UserExtra.objects.get(user=user)
    context = {
        'user':user
    }
    return render(request,'profile.html',context)