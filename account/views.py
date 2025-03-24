from django.shortcuts import render, redirect
from . import models
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
            return redirect('register')
        
        if User.objects.filter(email = email).exists():
            messages.error(request , "Email Already Exists")
            return redirect('register')
            
        if password != password2:
            messages.error(request , "password Doesn't Match")
            return redirect('register')
        
        user = User.objects.create(username=username,email=email)
        user.set_password(password)
        user.save()
        models.UserExtra.objects.create(user = user)
        messages.success(request, 'Your account has been created! ')
        
    return render(request , 'register.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():
            messages.error(request , "User Doesn't Exists")
            return redirect('login')
        
        user = User.objects.get(username = username)
        user_obj=None
        try:
            user_obj = models.UserExtra.objects.get(user = user)
        except:
            user_obj = authenticate(username = username, password = password)
            if not user_obj:
                messages.error(request, "Invalid Credential")
                return redirect('login') 
            login(request,user_obj)
            return redirect('/admin')
        
        if not user_obj.verified:
            messages.error(request, "Verification mail has been sent to email. Please Verify your account!")
            # return redirect('login')
        
        user_obj = authenticate(username=username, password=password)
        if not user_obj:
            messages.error(request, "Invalid Credential.")
            return redirect('login')
        login(request,user_obj)
        return redirect('home')
    return render(request , 'login.html')

def logoutpage(request):
    logout(request)
    return redirect('login')


