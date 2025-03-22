from django.shortcuts import render
from shop.models import *
from itertools import groupby
from operator import attrgetter
from math import ceil
# Create your views here.
 
def home(request):
    categories = ProductCategory.objects.all()
    products = [category.products.first() for category in categories if category.products.exists()]
    
    slides = [products[i:i+4] for i in range(0, len(products), 4)]
    cat = ProductCategory.objects.all().distinct()
    print(cat)
    context = {
        'products':products,
        'catogery':cat,
        'slides': slides
    }
    return render(request,'home.html',context)