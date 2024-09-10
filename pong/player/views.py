from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.middleware.csrf import get_token
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from .otp import send_otp, create_otp_code
from .jwt import generate_jwt, decode_jwt, token_user, set_jwt_token
from .forms import RegisterForm, ChangePasswordForm, UpdateForm
from .models import Player, BlacklistedToken
import os
import pyotp
import requests
import jwt
import json


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            if user is not None:
                login(request, user)
                user.nickname = user.username[1:]
                user.save()
                token = generate_jwt(user)
                response = HttpResponse(status=302)  # 302 redirect to another page
                response = redirect('/player/account/')
                set_jwt_token(response, token)

                print("JWT cookie set:", response.cookies['jwt'].value) 
                print("----------------------------------")

                return response

    else:
        form = RegisterForm()
    return render(request, 'player/register.html', {'form': form})


def username_underscore(request):
    post_data = request.POST.copy()
    raw_username = post_data.get('username')
    if raw_username:
        post_data['username'] = f"_{raw_username}"
    return post_data


def login_view(request):
    if request.method == "POST":
        post_data = username_underscore(request)
        form = AuthenticationForm(data=post_data)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if user is not None:
                user = get_object_or_404(Player, username=user.username)
                print(f"phone: {user.phone_number}")

                if not user.email_2fa_active and not user.sms_2fa_active:
                    token = generate_jwt(user)
                    user = decode_jwt(token)
                    print(user)
                    
                    if not user.nickname:
                        user.nickname = user.username[1:]
                        user.save()

                    response = HttpResponse(status=302)  # 302 redirect to another page
                    response = redirect('/player/account/')
                    set_jwt_token(response, token)

                    print("JWT cookie set:", response.cookies['jwt'].value)
                    print("----------------------------------")

                    return response
                
                response = HttpResponse(status=302)  # 302 redirect to another page
                response = redirect('/player/tfa/', {"user": user})
                return response

        elif '42_login' in request.POST:
            oauth_url = f"{settings.FT42_OAUTH_URL}?client_id={settings.FT42_CLIENT_ID}&redirect_uri={settings.FT42_REDIRECT_URI}&response_type=code"
            return redirect(oauth_url)

    else:
        form = AuthenticationForm()

    return render(request, 'player/login.html', {"form": form })



def login_42_view(request):
    oauth_url = f"{settings.FT42_OAUTH_URL}?client_id={settings.FT42_CLIENT_ID}&redirect_uri={settings.FT42_REDIRECT_URI}&response_type=code"
    
    return render(request, 'login_42.html', {'oauth_url': oauth_url})


def tfa_view(request):
    ########################### Here I use the user from request and call its Player object. I apply the JWT token only when the 2FA/OTP is valid
    if not request.user.is_authenticated:
        return redirect('/player/login/')
    try:
        user = get_object_or_404(Player, username=request.user.username)
    except Player.DoesNotExist:
        return redirect('/player/login/')

    print(f"username: {user.username}")
    print(f"phone_number: {user.phone_number}")
    ###########################

    if request.method == "POST":
        print(f"POST data: {request.POST}")

        if 'tfa' in request.POST:

            totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
                
            request.session['username'] = user.username
            request.session['otp_secret_key'] = totp.secret
            request.session['otp_valid_date'] = (datetime.now() + timedelta(minutes=1)).isoformat()
            
            print(f"request.session['username']: {request.session['username']}")
            print(f"request.session['otp_secret_key']: {request.session['otp_secret_key']}")
            print(f"request.session['otp_valid_date']: {request.session['otp_valid_date']}")
                
            otp_method = request.POST.get('otp_method')
            if  otp_method == 'sms':
                contact = str(user.phone_number)
                print("contact: " + contact)
                send_otp(request, totp, contact, method='sms')
            elif otp_method == 'email':
                contact = user.email
                print("contact: " + contact)
                send_otp(request, totp, contact, method='email')
            
            return redirect('/player/otp/')

    return render(request, 'player/tfa.html', {'user': user})


def otp_view(request):
    ########################### Here I use the user from request and call its Player object. I apply the JWT token only when the 2FA/OTP is valid
    if not request.user.is_authenticated:
        return redirect('/player/login/')
    try:
        user = get_object_or_404(Player, username=request.user.username)
    except Player.DoesNotExist:
        return redirect('/player/login/')

    print(f"username: {user.username}")
    print(f"phone_number: {user.phone_number}")
    ###########################

    if request.method == "POST":
        print(f"POST data: {request.POST}")
        if 'otp' in request.POST:
        
            user_otp = request.POST.get('otp')
            otp_secret_key = request.session.get('otp_secret_key')
            otp_valid_date = request.session.get('otp_valid_date')

            print(f"user_otp: {user_otp}" )
            print(f"otp_secret_key: {otp_secret_key}")
            print(f"otp_valid_date: {otp_valid_date}")

            if otp_secret_key and otp_valid_date:
                valid_until = datetime.fromisoformat(otp_valid_date)
                if valid_until > datetime.now():
                    totp = pyotp.TOTP(otp_secret_key, interval=60)
                    if totp.verify(user_otp):
                        token = generate_jwt(user)
                        response = HttpResponse(status=302)  # 302 redirect to another page
                        response = redirect('/player/account/')
                        set_jwt_token(response, token)
                        
                        del request.session['otp_secret_key']
                        del request.session['otp_valid_date']
                        del request.session['username']

                        return response
                else:
                    return render(request, 'player/otp.html', {'error': 'OTP has expired'})
            return render(request, 'player/otp.html', {'error': 'Invalid OTP'})
    return render(request, 'player/otp.html')


def auth_42_callback(request):
    code = request.GET.get('code')
    if not code:
        return redirect('/player/login/')

    token_url = 'https://api.intra.42.fr/oauth/token'
    data = {
        'grant_type': 'authorization_code',
        'client_id': settings.FT42_CLIENT_ID,
        'client_secret': settings.FT42_CLIENT_SECRET,
        'code': code,
        'redirect_uri': settings.FT42_REDIRECT_URI,
    }

    print('############################')
    print('client_id : ' + settings.FT42_CLIENT_ID)
    print('client_secret : ' + settings.FT42_CLIENT_SECRET)
    print('code : ' + code)
    print('redirect_uri : ' + settings.FT42_REDIRECT_URI)
    print('token_url : ' + token_url)

    response = requests.post(token_url, data=data)
    if response.status_code != 200: #if the HTTP request (get) is not successful 
        return redirect('/player/login/')

    token_info = response.json()
    access_token = token_info.get('access_token')
    if not access_token:
        return redirect('/player/login/')

    user_info_response = requests.get(
        'https://api.intra.42.fr/v2/me',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    if user_info_response.status_code != 200: #if the HTTP request (get) is not successful 
        return redirect('/player/login/')

    user_info = user_info_response.json()
    login = user_info.get('login')
    username = f'{login}'
    email = user_info.get('email')
    profile_picture = user_info["image"]["versions"]["small"]

    print('\n')
    print('login : ' + user_info.get('login'))
    print('email : ' + user_info.get('email'))
    print('last_name : ' + user_info.get('last_name'))
    print('############################')

    if not username:
        return redirect('/player/login/')

    user, created = Player.objects.get_or_create(
        username=username,
        defaults={'email': email}
    )
    
    if user is not None:
        user.student = True
        user.nickname = user.username
        user.save()
        if profile_picture: 
            response = requests.get(profile_picture)
            if response.status_code == 200: #if the HTTP request (get) is successful 
                picture_name = f"{user.username}_profile.jpg"
                profile_pic_dir = os.path.join(settings.MEDIA_ROOT, "profile_pictures", user.username)

                if not os.path.exists(profile_pic_dir):
                    os.makedirs(profile_pic_dir)
                    user.profile_picture.save(picture_name, ContentFile(response.content), save=True)
            else:
                print(f"Failed to fetch profile picture, status code: {response.status_code}")
        
        token = generate_jwt(user)
        response = redirect('/player/account/')
        set_jwt_token(response, token)
        user = token_user(request)
        
        return response

    return redirect('/player/account/')

def account_view(request):
    user = token_user(request)
    if request.method == 'POST':
        email_2fa_active = 'email_2fa_active' in request.POST
        sms_2fa_active = 'sms_2fa_active' in request.POST

        user.email_2fa_active = email_2fa_active
        if user.phone_number:
            user.sms_2fa_active = sms_2fa_active
        user.save()
    return render(request, 'player/account.html', {'user': user})


def update(request):
    user = token_user(request)

    if request.method == 'POST':
        form = UpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/player/account/')
    else:
        form = UpdateForm(instance=user)
    return render(request, 'player/update.html', {'form': form})


def update_password(request):
    user = token_user(request)

    if request.method == 'POST':
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('/player/account/')
        else:
            return render(request, 'player/update_password.html', {"form": form})
    else:
        form = ChangePasswordForm(user)
        return render(request, 'player/update_password.html', {"form": form})


def logout_view(request):
    token = request.COOKIES.get('jwt')
    response = redirect('/player/login/')
    if token:
        BlacklistedToken.objects.create(token=token)
        response.delete_cookie('jwt')
    logout(request)
    return response


def delete_account(request):
    user = token_user(request)
    return render(request, 'player/delete_account.html')