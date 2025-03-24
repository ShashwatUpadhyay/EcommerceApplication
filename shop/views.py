from django.shortcuts import render, HttpResponse , redirect
from django.http import JsonResponse
from . import models
from django.contrib import messages
from django.db.models import Q
from orders.models import Cart, CartItem
from shop.models import ProductImage
from django.core.paginator import Paginator

# Create your views here.

def shop(request):
    category = models.ProductCategory.objects.all()
    products = models.Product.objects.all()
    # print(request.user.extra in Cart.objects.filter(customer=request.user.extra, is_paid=False, cartitems__product__in=products))
    category_name = request.GET.get('category')
    sort = request.GET.get('sort')
    s = request.GET.get('s')
    
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
    
    if s:
        products = models.Product.objects.filter(Q(title__icontains = s)|Q(category__name__icontains = s)|Q(subcategory__name__icontains = s))
        p = Paginator(products,6)
        page = request.GET.get('page')
        products = p.get_page(page)
        return render(request , 'shop.html',{'products':products, 'categories': category})

    if category_name == 'all' or category_name == '' or not category_name:
        if sort == 'az':
            products = models.Product.objects.all().order_by('title')
        elif sort == 'new':
            products = models.Product.objects.all().order_by('-created_at')
        elif sort == 'lh':
            products = models.Product.objects.all().order_by('price')
        elif sort == 'hl':
            products = models.Product.objects.all().order_by('-price')
        
        p = Paginator(products,6)
        page = request.GET.get('page')
        products = p.get_page(page)
        return render(request , 'shop.html',{'products':products, 'categories': category})

    if category_name:
        products = models.Product.objects.filter(Q(category = category_obj)|Q(subcategory = sub_category_obj))
    else:
        products = models.Product.objects.all()
        
    if sort == 'az':
        products = models.Product.objects.filter(Q(category = category_obj)|Q(subcategory = sub_category_obj)).order_by('title')
    elif sort == 'new':
        products = models.Product.objects.filter(Q(category = category_obj)|Q(subcategory = sub_category_obj)).order_by('created_at')        
    elif sort == 'lh':
        products = models.Product.objects.filter(Q(category = category_obj)|Q(subcategory = sub_category_obj)).order_by('price')  
    elif sort == 'hl':
        products = models.Product.objects.filter(Q(category = category_obj)|Q(subcategory = sub_category_obj)).order_by('-price')
    try:    
        if sort == 'az':
            products = models.Product.objects.filter(Q(category = category_obj)|Q(subcategory = sub_category_obj)).order_by('title')
        elif sort == 'new':
            products = models.Product.objects.filter(Q(category = category_obj)|Q(subcategory = sub_category_obj)).order_by('created_at')
        elif sort == 'lh':
            products = models.Product.objects.filter(Q(category = category_obj)|Q(subcategory = sub_category_obj)).order_by('price')
        elif sort == 'hl':
            products = models.Product.objects.filter(Q(category = category_obj)|Q(subcategory = sub_category_obj)).order_by('-price')
    except Exception as e:
        print(e)
        messages.error(request , "Product Not Found")
    
    p = Paginator(products,6)
    page = request.GET.get('page')
    products = p.get_page(page)
    
    return render(request , 'shop.html',{'products':products, 'categories': category})

def search_suggestions(request):
    query = request.GET.get('s', '')
    if query:
        products = models.Product.objects.filter(Q(title__icontains=query)|Q(category__name__icontains=query)|Q(subcategory__name__icontains=query))[:5]  
        category = models.ProductCategory.objects.filter(Q(name__icontains=query))[:5]  
        subcategory = models.ProductSubCategory.objects.filter(Q(name__icontains=query)|Q(category__name__icontains=query))[:5]  
        results = list(products.values('title', 'slug','price','uid','image'))  
        categories = list(category.values('name', 'slug','uid','img'))  
        subcategories = list(subcategory.values('name', 'slug','uid'))  
        return JsonResponse({'products': results,'categories':categories,'subcategories':subcategories}) 
    return JsonResponse({'results': [],'categories':[],'subcategories':[]}) 

def get_img(request, uid):
    image = ProductImage.objects.get(uid=uid)
    return JsonResponse({'image_url': image.img.url})



def product_page(request, slug):
    cart = None
    product = None
    cart_item = CartItem.objects.all()
    try:
        product = models.Product.objects.get(slug=slug)
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
    
