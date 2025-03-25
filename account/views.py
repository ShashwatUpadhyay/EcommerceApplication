from django.shortcuts import render, redirect
from . import models
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils import timezone
from .helper import send_forget_password_email
import uuid
from django.contrib.auth.hashers import check_password
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


def address_edit(request, uid):
    address = models.Address.objects.get(uid=uid)
    if request.method == 'POST':
        if request.POST.get('selected'):
            models.Address.objects.filter(user=request.user).update(selected=False)
        address.email = request.POST.get('email')
        address.full_name = request.POST.get('full_name')
        address.address = request.POST.get('address')
        address.country = request.POST.get('country')
        address.city = request.POST.get('city')
        address.state = request.POST.get('state')
        address.pin_code = request.POST.get('zipcode')
        address.phone = request.POST.get('phone')
        address.selected = True if request.POST.get('selected') else False
        print(request.POST.get('selected'))
        
        address.save()
        return redirect('profile')
    return render(request, 'address_edit.html', {'address':address})

def add_address(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        country = request.POST.get('country')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pin_code = request.POST.get('zipcode')
        phone = request.POST.get('phone')
        selected = request.POST.get('selected')
        if selected:
            models.Address.objects.filter(user=request.user).update(selected=False)
        models.Address.objects.create(user=request.user, email=email, full_name=full_name, address=address, country=country, city=city, state=state, pin_code=pin_code, phone=phone, selected=  True if selected else False)
        messages.success(request, 'Address added successfully.')
        return redirect('profile')
    return render(request, 'add_address.html')

def delete_address(request, uid):
    address = models.Address.objects.get(uid=uid)   
    address.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def ForgetPassword(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            if not User.objects.filter(email=email).exists():
                messages.error(request, "Email Doesn't Exists")
                return redirect('password_reset')
            token = uuid.uuid4()
            user = User.objects.get(email=email)
            user_extra = models.UserExtra.objects.get(user=user)
            user_extra.forgot_password_token = token
            user_extra.forgot_password_token_created_at = timezone.now()
            user_extra.save()
            send_forget_password_email(email, token)
            messages.info(request, "An email is sent to your email. Please reset your password.")
            return redirect('password_reset')
    except Exception as e:
        print(e)
    
    return render(request, 'registration/pass_reset_form.html')


def change_password(request,token):
    context = {}
    try:
        
        profile_obj = models.UserExtra.objects.get(forgot_password_token=token)
        if profile_obj.forgot_password_token != token:
            messages.error(request, "Invalid Request")
            context = {
            'user_id': None
            }
        
            return render(request, 'registration/pass_reset_confirm.html',)
            
        if request.method == 'POST':
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            user_id = request.POST.get('user_id')
            if user_id is None:
                messages.error(request, "Invalid Request")
                return redirect('password_reset_confirm', token=token)
            if password != password2:
                messages.error(request, "Password Doesn't Match")
                return redirect('password_reset_confirm', token=token)
            user = profile_obj.user
            user.set_password(password)
            user.save()
            profile_obj.forgot_password_token = None
            profile_obj.forgot_password_token_created_at = None
            profile_obj.save()
            messages.success(request, "Password Changed Successfully")
            return redirect('login')
        
        
        
        context = {
            'user_id': profile_obj.user.id
        }
        
        
    except Exception as e:
        print(e)    
    return render(request, 'registration/pass_reset_confirm.html',context)


from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

@login_required
def UserPassChange(request):
    try:
        if request.method == 'POST':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            new_password2 = request.POST.get('confirm_password')
            user = request.user

            if not user.check_password(old_password):
                messages.error(request, "Old Password is Incorrect")
                return redirect('passchange')

            if new_password != new_password2:
                messages.error(request, "Passwords do not match!")
                return redirect('passchange')

            # try:
            #     validate_password(new_password, user)
            # except ValidationError as e:
            #     messages.error(request, " ".join(e.messages))
            #     return redirect('passchange')

            user.set_password(new_password)
            user.save()

            update_session_auth_hash(request, user)

            messages.success(request, "Password Changed Successfully")
            return redirect('profile')
    except Exception as e:
        print(e)

    return render(request, 'userpass_change.html')


