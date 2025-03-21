from django.shortcuts import render, HttpResponse , redirect
from . import models
from django.contrib import messages
# Create your views here.

def shop(request):
    category = models.ProductCategory.objects.all()
    products = models.Product.objects.all()
    
    category_name = request.GET.get('category')
    sort = request.GET.get('sort')
    
    if category_name == 'all':
        return render(request , 'shop.html',{'products':products, 'categories': category})

    category_obj = None
    try:
        category_obj = models.ProductSubCategory.objects.get(name=category_name)
        products = models.Product.objects.filter(subcategory = category_obj)
        if sort == 'az':
            products = models.Product.objects.filter(subcategory = category_obj).order_by('title')
            print(sort)
        elif sort == 'new':
            products = models.Product.objects.filter(subcategory = category_obj).order_by('created_at')
            print(sort)
            
        elif sort == 'lh':
            products = models.Product.objects.filter(subcategory = category_obj).order_by('price')
            print(sort)
            
        elif sort == 'hl':
            products = models.Product.objects.filter(subcategory = category_obj).order_by('-price')
            print(sort)
            
        return render(request , 'shop.html',{'products':products, 'categories': category})
            
    except:
        pass
    try:
        category_obj = models.ProductCategory.objects.get(name=category_name)
        products = models.Product.objects.filter(category = category_obj)
        return render(request , 'shop.html',{'products':products, 'categories': category})
    except:
        messages.error(request , "Product Not Found")
    
    return render(request , 'shop.html',{'products':products, 'categories': category})

def product_page(request, slug):
    try:
        product = models.Product.objects.get(slug=slug)
    except Exception as e:
        print(e)
        return HttpResponse("Product NOt Found!")
    return render(request, 'product.html', {'product':product})
    