from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from .utils import send_otp, create_otp_code, create_qr_code
from .forms import RegisterForm, PhoneForm
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

            otp_method = request.POST.get('otp_method')
            use_sms = otp_method == 'sms'
            use_email = otp_method == 'email'

            totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
            request.session['username'] = user.username
            request.session['otp_secret_key'] = totp.secret
            request.session['otp_valid_date'] = (datetime.now() + timedelta(minutes=1)).isoformat()

            if use_sms:
                send_otp(request, totp, method='sms')
            elif use_email:
                send_otp(request, totp, metho='email')
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
        return redirect('/player/login/')
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
