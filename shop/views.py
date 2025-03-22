from django.shortcuts import render, HttpResponse , redirect
from . import models
from django.contrib import messages
from django.db.models import Q

# Create your views here.

def shop(request):
    category = models.ProductCategory.objects.all()
    products = models.Product.objects.all()
    
    category_name = request.GET.get('category')
    sort = request.GET.get('sort')
    
    category_obj = None
    sub_category_obj = None
    try:
        sub_category_obj = models.ProductSubCategory.objects.get(slug=category_name)
    except models.ProductSubCategory.DoesNotExist:
        sub_category_obj = None

    try:
        category_obj = models.ProductCategory.objects.get(slug=category_name)
    except models.ProductCategory.DoesNotExist:
        category_obj = None
    
    if category_name == 'all':
        if sort == 'az':
            products = models.Product.objects.all().order_by('title')
            print(sort)
        elif sort == 'new':
            products = models.Product.objects.all().order_by('created_at')
            print(sort)
            
        elif sort == 'lh':
            products = models.Product.objects.all().order_by('price')
            print(sort)
            
        elif sort == 'hl':
            products = models.Product.objects.all().order_by('-price')
            print(sort)
        return render(request , 'shop.html',{'products':products, 'categories': category})

    if category_name:
        products = models.Product.objects.filter(Q(category = category_obj)|Q(subcategory = sub_category_obj))
    else:
        products = models.Product.objects.all()
    if sort == 'az':
        products = models.Product.objects.filter(Q(category = category_obj)|Q(subcategory = sub_category_obj)).order_by('title')
        print(sort)
    elif sort == 'new':
        products = models.Product.objects.filter(Q(category = category_obj)|Q(subcategory = sub_category_obj)).order_by('created_at')
        print(sort)
        
    elif sort == 'lh':
        products = models.Product.objects.filter(Q(category = category_obj)|Q(subcategory = sub_category_obj)).order_by('price')
        print(sort)
        
    elif sort == 'hl':
        products = models.Product.objects.filter(Q(category = category_obj)|Q(subcategory = sub_category_obj)).order_by('-price')
        print(sort)

    try:    
        if sort == 'az':
            products = models.Product.objects.filter(Q(category = category_obj)|Q(subcategory = sub_category_obj)).order_by('title')
            print(sort)
        elif sort == 'new':
            products = models.Product.objects.filter(Q(category = category_obj)|Q(subcategory = sub_category_obj)).order_by('created_at')
            print(sort)
            
        elif sort == 'lh':
            products = models.Product.objects.filter(Q(category = category_obj)|Q(subcategory = sub_category_obj)).order_by('price')
            print(sort)
            
        elif sort == 'hl':
            products = models.Product.objects.filter(Q(category = category_obj)|Q(subcategory = sub_category_obj)).order_by('-price')
            print(sort)
        # return render(request , 'shop.html',{'products':products, 'categories': category})
    except Exception as e:
        print(e)
        messages.error(request , "Product Not Found")
    
    return render(request , 'shop.html',{'products':products, 'categories': category})

def product_page(request, slug):
    try:
        product = models.Product.objects.get(slug=slug)
    except Exception as e:
        print(e)
        return HttpResponse("Product NOt Found!")
    return render(request, 'product.html', {'product':product})
    