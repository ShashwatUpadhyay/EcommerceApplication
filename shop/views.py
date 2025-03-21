from django.shortcuts import render, HttpResponse
from . import models
# Create your views here.

def shop(request):
    products = models.Product.objects.all()
    return render(request , 'shop.html',{'products':products})

def product_page(request, slug):
    try:
        product = models.Product.objects.get(slug=slug)
    except Exception as e:
        print(e)
        return HttpResponse("Product NOt Found!")
    return render(request, 'product.html', {'product':product})
    