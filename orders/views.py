from django.shortcuts import render , HttpResponse, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from . import models
from shop.models import Product
from django.contrib import messages
from account.models import Address
# Create your views here.

def order(request):
    return HttpResponse(request, "This order home page")

@login_required(login_url='login')
def addToCart(request):
    customer = request.user
    product_id = request.GET.get('product_id')
    try:
        cart , _ = models.Cart.objects.get_or_create(customer = customer.extra, is_paid = False)
        cart_item , _ = models.CartItem.objects.get_or_create(cart = cart , product=Product.objects.get(uid = product_id))
        cart_item.quantity += 1
        cart_item.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        print(e)
        messages.error(request, "Invalid Product ID")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def removeFromCart(request):
    customer = request.user
    product_id = request.GET.get('product_id')
    try:
        cart , _ = models.Cart.objects.get_or_create(customer = customer.extra, is_paid = False)
        cart_item = models.CartItem.objects.filter(cart = cart , product=Product.objects.get(uid = product_id))
        
        if cart_item.exists():
            cart_item = cart_item[0]
            cart_item.quantity -= 1
            
            if cart_item.quantity <= cart_item.product.min_order_quanitity-1:
                cart_item.delete()
            else:
                cart_item.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        print(e)
        messages.error(request, "Invalid Product ID")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
@login_required(login_url='login')
def removeItem(request):
    customer = request.user
    product_id = request.GET.get('product_id')
    try:
        cart , _ = models.Cart.objects.get_or_create(customer = customer.extra, is_paid = False)
        cart_item = models.CartItem.objects.filter(cart = cart , product=Product.objects.get(uid = product_id))
        
        if cart_item.exists():
            cart_item = cart_item[0]
            cart_item.delete()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        print(e)
        messages.error(request, "Invalid Product ID")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
 
@login_required(login_url='login')   
def cart(request):
    customer = request.user
    product_id = request.GET.get('product_id')
    cart_item=None
    
    try:
        cart = models.Cart.objects.get(customer = customer.extra, is_paid = False)
        cart_item = models.CartItem.objects.filter(cart = cart)
        total_price = cart.total_price
        tax = cart.tax
        final_price = cart.final_price
    except Exception as e:
        print(e)
    return render(request , 'cart.html',{'cart_items':cart_item,'total_price':total_price,'tax':tax,'final_price':final_price})

@login_required(login_url='login')   
def shipping(request):
    ads = Address.objects.filter(user=request.user)
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        address = request.POST.get('address')
        zipcode = request.POST.get('zipcode')
        phone = request.POST.get('phone')
        print(country,
            state,
            city,
            address,
            zipcode,
            full_name,
            email,
            phone
            )
        ads = Address.objects.create(user = request.user,
                                     state = state,
                                    city = city,
                                    address = address,
                                    pip_code = zipcode,
                                    full_name = full_name,
                                    email = email,
                                    phone = phone
                                     )
        return redirect('')
    return render(request, 'shipping.html',{'ads':ads})



@login_required(login_url='login')   
def payment(request):
    return render(request , 'payment.html')