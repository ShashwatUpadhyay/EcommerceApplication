from django.shortcuts import render, redirect, get_object_or_404
from shop.models import *
from account.models import UserExtra
from django.contrib.auth.decorators import login_required
from account.models import Address
from orders.models import Order
from .rabbitmq import publish_message
# Create your views here.
def is_staff(request):
    return request.user.is_staff

def home(request):
    publish_message("hellow")
    categories = ProductCategory.objects.all()
    products = [category.products.first() for category in categories if category.products.exists()]
    
    slides = [products[i:i+4] for i in range(0, len(products), 2)]  
    cat = ProductCategory.objects.all().distinct()
    # print(request.headers)
    context = {
        'products': products,
        'catogery': cat,
        'slides': slides
    }

    return render(request,'home.html',context)

@login_required(login_url='login')
def profile(request):
    user = request.user
    user = UserExtra.objects.get(user=user)
    # address = Address.objects.filter(user=user)
    context = {
        'user':user,
        # 'address':address,
    }
    return render(request,'profile.html',context)

def track(request):
    if request.method == 'POST':
        order_number = request.POST.get('order_number')
        return redirect('track_order' , number = order_number)
    return render(request, 'track_order.html')

def track_order(request,number):
    order = get_object_or_404(Order, order_number = number)
    return render(request, 'track.html', {'order':order})

