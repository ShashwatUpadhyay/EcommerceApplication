from django.shortcuts import render, HttpResponse , redirect
from . import models
from django.contrib import messages
from django.db.models import Q
from orders.models import Cart, CartItem
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
    
    if category_name == 'all' or category_name == '':
        if sort == 'az':
            products = models.Product.objects.all().order_by('title')
            print(sort)
        elif sort == 'new':
            products = models.Product.objects.all().order_by('-created_at')
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
        cart = None
        cart_item = None
        if request.user.is_authenticated:
            cart = Cart.objects.get(customer=request.user.extra)
            cart_item = CartItem.objects.filter(cart=cart, product = product)
    except Exception as e:
        print(e)
    item_count=None
    exist = False
    if request.user.is_authenticated:
        if cart_item.exists():
            exist = True
        if cart_item:
            item_count = cart_item[0].quantity
        else:
            item_count = 0
    else:
        exist = False
        item_count = 0
    return render(request, 'product.html', {'product':product, 'item_count': item_count, 'exist':exist })
    