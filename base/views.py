from django.shortcuts import render
from shop.models import Product
# Create your views here.
 
def home(request):
    products = Product.objects.all()
    cat = Product.objects.all().values('category__name').distinct()
    context = {
        'products':products
    }
    return render(request,'home.html',context)