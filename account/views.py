from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        print(email, username, password, password2)
        if User.objects.filter(username = username).exists():
            messages.error(request , "Username Already Exists")
        if User.objects.filter(email = email).exists():
            messages.error(request , "Email Already Exists")
            
    return render(request , 'register.html')

def login_page(request):
    return render(request , 'login.html')