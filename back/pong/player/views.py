from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .utils import send_otp
from datetime import datetime
from .forms import RegisterForm
from .models import Player
import pyotp

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
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            send_otp(request)
            request.session['username'] = user.username
            return redirect('/player/otp/')
    else:
        form = AuthenticationForm()
    return render(request, 'player/login.html', {"form": form})

def otp_view(request):
    if request.method == "POST":
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

                    # Clear session data
                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']
                    del request.session['username']

                    return redirect('/about/')
            else:
                return render(request, 'player/otp.html', {'error': 'OTP has expired'})

        return render(request, 'player/otp.html', {'error': 'Invalid OTP'})

    return render(request, 'player/otp.html')
