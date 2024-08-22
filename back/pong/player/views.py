from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from .otp import send_otp, create_otp_code, create_qr_code
from .forms import RegisterForm, PhoneForm
from .models import Player
import pyotp
import requests
from django.conf import settings

import json
from django.core.exceptions import ImproperlyConfigured

with open("secrets.json") as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        raise ImproperlyConfigured(f"Set the {setting} environment variable.")

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect(f'/player/success/?username={user.username}')
    else:
        form = RegisterForm()
    return render(request, 'player/register.html', {'form': form})

def success_view(request):
    username = request.GET.get('username')
    user = get_object_or_404(Player, username=username)
    context = {
        'user': user,
        'phone_number': user.phone_number,
    }
    return render(request, 'player/success.html', context)

def login_view(request):
    if request.method == "POST":
        if 'login' in request.POST:
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()

                otp_method = request.POST.get('otp_method')
                totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
                request.session['username'] = user.username
                request.session['otp_secret_key'] = totp.secret
                request.session['otp_valid_date'] = (datetime.now() + timedelta(minutes=1)).isoformat()
               
                print("username: " + request.session['username'])
                print("otp_secret_key: " + request.session['otp_secret_key'])
                print("otp_valid_date: " + request.session['otp_valid_date'])

                if  otp_method == 'sms':
                    contact = str(user.phone_number)
                    print("contact: " + contact)
                    send_otp(request, totp, contact, method='sms')
                elif otp_method == 'email':
                    contact = user.email
                    print("contact: " + contact)
                    send_otp(request, totp, contact, method='email')
                return redirect('/player/otp/')
        #else:
            #auth_url = f"https://api.intra.42.fr/oauth/authorize?client_id={settings.FT42_CLIENT_ID}&redirect_uri={settings.FT42_REDIRECT_URI}&response_type=code"
            #return render(request, auth_url)
             #   redirect_uri = settings.FT42_REDIRECT_URI
              #  client_id = settings.FT42_CLIENT_ID
               # auth_url = f"https://api.intra.42.fr/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
                #return redirect(auth_url)
    else:
        form = AuthenticationForm()
    return render(request, 'player/login.html', {"form": form})

def otp_view(request):
    if request.method == "POST":
        #if 'Resend_code':
        #    send_otp(request, totp, method='sms')

        user_otp = request.POST.get('otp')
        otp_secret_key = request.session.get('otp_secret_key')
        otp_valid_date = request.session.get('otp_valid_date')

        if otp_secret_key and otp_valid_date:
            valid_until = datetime.fromisoformat(otp_valid_date)

            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)
                if totp.verify(user_otp):
                    username = request.session.get('username')
                    user = get_object_or_404(Player, username=username)
                    login(request, user)

                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']
                    del request.session['username']

                    return redirect(f'/player/account/?username={user.username}')
            else:
                return render(request, 'player/otp.html', {'error': 'OTP has expired'})
        return render(request, 'player/otp.html', {'error': 'Invalid OTP'})
    return render(request, 'player/otp.html')


def display_qr_view(request):
    totp_secret_key = request.session.get('otp_secret_key')
    if not totp_secret_key:
        return redirect('/player/account/')
    totp = pyotp.TOTP(totp_secret_key, interval=60)
    qr_data = create_qr_code(request, totp)
    return render(request, 'player/display_qr.html', {'qr_data': qr_data})


@login_required
def account_view(request):
    user = request.user
    player = get_object_or_404(Player, username=user.username)

    if request.method == 'POST':
        form = PhoneForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect(f'/player/account/?username={user.username}')
    else:
        form = PhoneForm(instance=player)

    return render(request, 'player/account.html', {'form': form})


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
    if response.status_code != 200:
        return redirect('/player/login/')

    token_info = response.json()
    access_token = token_info.get('access_token')
    if not access_token:
        return redirect('/player/login/')

    user_info_response = requests.get(
        'https://api.intra.42.fr/v2/me',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    if user_info_response.status_code != 200:
        return redirect('/player/login/')

    user_info = user_info_response.json()
    username = user_info.get('login')
    email = user_info.get('email')

    print('\n')
    print('login : ' + user_info.get('login'))
    print('email : ' + user_info.get('email'))
    print('last_name : ' + user_info.get('last_name'))
    print('############################')

    user, created = Player.objects.get_or_create(
        username=username,
        defaults={'email': email}
    )

    login(request, user)
    return redirect(f'/player/account/?username={user.username}')


@login_required
def logout_view(request):
    logout(request)
    return redirect(f'/player/login/')
