from django.shortcuts import render
from shop.models import Product
# Create your views here.
 
def home(request):
    return render(request,'home.html')