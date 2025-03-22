from django.shortcuts import render
from shop.models import *
# Create your views here.
 
def home(request):
    products = Product.objects.all()
    cat = ProductCategory.objects.all().distinct()
    print(cat)
    context = {
        'products':products,
        'catogery':cat
    }
    return render(request,'home.html',context)