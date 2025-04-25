from django.shortcuts import render, HttpResponse , redirect
from django.http import JsonResponse,HttpResponseRedirect
from . import models
from django.contrib import messages
from django.db.models import Q
from orders.models import Cart, CartItem
from shop.models import ProductImage
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required 
from base.views import is_staff
from django.views.decorators.csrf import csrf_exempt
from shop.models import Product



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
        p = Paginator(products,12)
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
        
        p = Paginator(products,12)
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
    
    p = Paginator(products,12)
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
            cart = Cart.objects.get(customer=request.user.extra,order_taken=False)
            if cart:
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

@login_required(login_url='login')
def stockManage(request):
    if not is_staff(request):
        return redirect('home')
    products = models.Product.objects.all()
    categories = models.ProductCategory.objects.all()
    
    if request.method == 'POST':
        stock = request.POST.get('stock')
        category = request.POST.get('category')
        search = request.POST.get('s')
        if stock:
            if stock == 'low_stock':
                print(stock, True)
                products = models.Product.objects.filter(stock__lte=9).order_by('-stock')
            elif stock == 'in_stock':
                print(stock, True)
                products = models.Product.objects.filter(stock__gte=10)
            elif stock == 'out_of_stock':
                print(stock, True)
                products = models.Product.objects.filter(stock=0)
                for p in products:
                    print(p.title)           
            else:
                print(stock, True)
                products = models.Product.objects.all()
            
        if category:
            if category=='all':
                products = models.Product.objects.all()
            else:
                products = models.Product.objects.filter(category__slug=category)
        
        if search:
            products = models.Product.objects.filter(Q(title__icontains=search)|Q(category__name__icontains=search)|Q(subcategory__name__icontains=search))
            
    p = Paginator(products,10)
    page = request.GET.get('page')
    products = p.get_page(page)
            
        
    return render(request , 'admin/stockmanage.html',{'products':products,'categories':categories})

@login_required(login_url='login')
def productEdit(request, uid):
    if not is_staff(request):
        return redirect('home')
    product = models.Product.objects.get(uid=uid)
    categories = models.ProductCategory.objects.all()
    subcategories = models.ProductSubCategory.objects.all()
    
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        subcategory = request.POST.get('subcategory')
        price = request.POST.get('price')
        min_order_quantity = request.POST.get('min_order_quantity')
        stock = request.POST.get('stock')
        main_image = request.POST.get('main_image')
        gallery_img = request.POST.get('gallery_img')
        print(title,
            description,
            category,
            subcategory,
            price,
            min_order_quantity,
            stock)
    return render(request , 'admin/productEdit.html',{'product':product,'categories':categories,'subcategories':subcategories})



# add to wishlist
@login_required(login_url='login')
def add_to_wishlist(request, uid):
    product = models.Product.objects.get(uid=uid)
    wishlist = models.Whislist.objects.filter(user=request.user, product=product).first()
    if wishlist:
        messages.error(request , "Product already in wishlist")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        models.Whislist.objects.create(user=request.user, product=product)
        messages.success(request , "Product added to wishlist")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
@login_required(login_url='login')
def wishlist(request):
    wishlist = models.Whislist.objects.filter(user=request.user)
    return render(request , 'wishlist.html',{'wishlist_items':wishlist})

@login_required(login_url='login')
def remove_wishlist(request, uid):
    try:
        wishlist = models.Whislist.objects.get(product = models.Product.objects.get(uid=uid),user=request.user)
        wishlist.delete()
        messages.success(request , "Product removed from wishlist")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except models.Whislist.DoesNotExist:
        print("Wishlist item does not exist")
        messages.error(request , "Product not found in wishlist")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    

    