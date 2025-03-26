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
from ecom.emails import order_successful
from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from ecom.settings import DOMAIN_NAME



razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


# Create your views here.

def order(request, uid):
    try:
        order = models.Order.objects.get(uid=uid)
    except Exception as e:
        print(e)
        return HttpResponse("Order not found", status=404)  # ✅ Proper error response
    return render(request, 'order.html', {'order': order})

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
        cart , _ = models.Cart.objects.get_or_create(customer = customer.extra, order_taken=False)
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
        cart , _ = models.Cart.objects.get_or_create(customer = customer.extra, order_taken = False)
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
    cart=None
    try:
        cart = models.Cart.objects.get(customer = request.user.extra,order_taken=False)
    except Exception as e:
        print(e)
        return redirect('cart')
    return render(request, 'shipping.html',{'ads':ads, 'cart':cart})


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

    
from django.urls import reverse

@login_required(login_url='login')
def payment(request):
    cart=None
    try:
        cart = models.Cart.objects.get(customer = request.user.extra,order_taken=False)
    except Exception as e:
        print(e)
        return redirect('cart')

    currency = 'INR'
    amount = int(cart.final_price * 100 )

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='1'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = request.build_absolute_uri(
        reverse('paymenthandler', kwargs={'uid': cart.uid})
    )


    # callback_url = '/payment/paymenthandler'



    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['cart'] = cart

    return render(request , 'payment.html', context=context)

@csrf_exempt
def paymenthandler(request, uid):
    try:
        cart = models.Cart.objects.get(uid=uid)
    except Exception as e:
        print(f"Cart error: {e}")
        messages.error(request, "Invalid Cart ID")
        return redirect('cart')  # Make sure 'cart' is a valid URL name

    if request.method != "POST":
        messages.error(request, "Invalid Request Method")
        return redirect('cart')

    try:
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        print(payment_id, razorpay_order_id, signature)
        if not all([payment_id, razorpay_order_id, signature]):
            messages.error(request, "Missing payment parameters")
            return redirect('cart')

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        print(params_dict)
        # Verify signature
        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
        except Exception as e:
            print(f"Signature verification error: {e}")
            messages.error(request, "Payment verification error")
            return render(request, 'paymentfail.html')

        # Check if payment already exists
        if models.Order.objects.filter(razorpay_payment_id=payment_id).exists():
            messages.warning(request, "This payment was already processed")
            return redirect('order_place')  # Or wherever you want to redirect

        amount = int(cart.final_price * 100)
        print(amount)
        
        try:
            # Check payment status before capturing
            payment = razorpay_client.payment.fetch(payment_id)
            if payment['status'] == 'captured':
                messages.info(request, "Payment was already captured")
            else:
                razorpay_client.payment.capture(payment_id, amount)
            
            # Update order
            order = models.Order.objects.create(
                user = cart.customer.user,
                cart=cart,
                is_paid=True,
                payment_id=payment_id,
                razorpay_order_id=razorpay_order_id,
                razorpay_payment_id=payment_id,
                razorpay_signature=signature,
                status='Processing'
            )
            print(order)

            # Update cart
            cart.is_paid = True
            cart.save()

            messages.success(request, "Payment successful!")
            return redirect('order_place')  # Ensure this URL name exists

        except razorpay.errors.BadRequestError as e:
            if 'already captured' in str(e):
                messages.warning(request, "Payment was already processed")
                return redirect('order_place')
            print(f"Razorpay capture error: {e}")
            messages.error(request, "Payment processing failed")
            return render(request, 'paymentfail.html')

    except Exception as e:
        print(f"General error: {e}")
        messages.error(request, "Payment processing error occurred")
        return redirect('cart')
    

@login_required(login_url='login')
def order_place(request):
    customer = request.user
    print(customer)
    try:

        address = Address.objects.get(user = customer, selected = True)
        print(address)
        cart = models.Cart.objects.get(customer = customer.extra,order_taken=False)
        order,_ = models.Order.objects.get_or_create(user = customer, cart = cart)
        order.address = address
        if _ :
            order.is_paid = False
        order.save()
        
        cart.order_taken = True
        cart.save()
        
        # order_successful(order)
        messages.success(request, "Your order has been placed successfully.")
        return redirect('home')
    except Exception as e:
        print(e)
        messages.error(request, "Invalid Product ID")

        return redirect('home')
    
