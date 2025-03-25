from django.shortcuts import render , HttpResponse, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from . import models
from shop.models import Product
from django.contrib import messages
from account.models import Address
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
import json

# Create your views here.

def order(request,  uid):
    try:
        order = models.Order.objects.get(uid = uid)
    except Exception as e:
        print(e)
    return render(request , 'order.html',{'order':order})

@login_required(login_url='login')
def my_orders(request):
    order = models.Order.objects.filter(user = request.user).order_by('-created_at')
    p = Paginator(order,3)
    page = request.GET.get('page')
    order = p.get_page(page)
    return render(request , 'myorders.html',{ 'orders':order})

@login_required(login_url='login')
def my_orders_ordersprocessing(request):
    order = models.Order.objects.filter(user = request.user, status = 'Processing').order_by('-created_at')
    p = Paginator(order,3)
    page = request.GET.get('page')
    order = p.get_page(page)
    return render(request , 'ordersprocessing.html',{ 'orders':order})

@login_required(login_url='login')
def my_orders_ordershipped(request):
    order = models.Order.objects.filter(user = request.user, status = 'Shipped').order_by('-created_at')
    p = Paginator(order,3)
    page = request.GET.get('page')
    order = p.get_page(page)
    return render(request , 'ordershipped.html',{ 'orders':order})

@login_required(login_url='login')
def my_orders_orderdelivered(request):
    order = models.Order.objects.filter(user = request.user, status = 'Delivered').order_by('-created_at')
    p = Paginator(order,3)
    page = request.GET.get('page')
    order = p.get_page(page)
    return render(request , 'orderdelivered.html',{ 'orders':order})

@login_required(login_url='login')
def my_orders_ordercanceled(request):
    order = models.Order.objects.filter(user = request.user, status = 'Canceled').order_by('-created_at')
    p = Paginator(order,3)
    page = request.GET.get('page')
    order = p.get_page(page)
    return render(request , 'ordercanceled.html',{ 'orders':order})

@login_required(login_url='login')
def addToCart(request):
    customer = request.user
    product_id = request.GET.get('product_id')
    try:
        cart , _ = models.Cart.objects.get_or_create(customer = customer.extra,order_taken=False, is_paid = False)
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
    total_price=0
    tax=0
    final_price=0
    try:
        cart = models.Cart.objects.get(customer = customer.extra,order_taken=False, is_paid = False)
        cart_item = models.CartItem.objects.filter(cart = cart)
        total_price = cart.total_price if cart else 0
        tax = cart.tax if cart else 0
        final_price = cart.final_price if cart else 0
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

        if full_name and email and country and state and city and address and zipcode and phone:
            ads = Address.objects.create(user = request.user,country=country,state = state,city = city,address = address,pin_code = zipcode,full_name = full_name,email = email,phone = phone, selected = True)
        
        return redirect('payment')
    return render(request, 'shipping.html',{'ads':ads})


@csrf_exempt  # Disable CSRF for simplicity (use proper authentication in production)
def select_address(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            address_uid = data.get("address_uid")
            user = request.user  # Get the logged-in user

            # Unselect all addresses
            Address.objects.filter(user=user).update(selected=False)

            # Set the selected address
            selected_address = get_object_or_404(Address, uid=address_uid, user=user)
            selected_address.selected = True
            selected_address.save()

            return JsonResponse({"success": True, "message": "Address updated successfully!"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request"})


@login_required(login_url='login')   
def payment(request):
    return render(request , 'payment.html')

@login_required(login_url='login')
def order_place(request):
    customer = request.user
    try:
        cart = models.Cart.objects.get(customer = customer.extra,order_taken=False,is_paid = False)
        address = Address.objects.get(user = customer, selected = True)
        order = models.Order.objects.create(user = customer, address = address, cart = cart)
        cart.order_taken = True
        cart.save()
        order.status='Processing'
        order.save()
        messages.success(request, "Your order has been placed successfully.")
        return redirect('home')
    except Exception as e:
        print(e)
        messages.error(request, "Invalid Product ID")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
