from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.middleware.csrf import get_token
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from .otp import send_otp, create_otp_code, create_qr_code
from .jwt import generate_jwt, decode_jwt
from .forms import RegisterForm, PhoneForm
from .models import Player, BlacklistedToken
import pyotp
import requests
import jwt
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
            
            if user is not None:
                token = generate_jwt(user)
                print("token: " + token)
                return JsonResponse({'token': token})
            #login(request, user)
            #return redirect(f'/player/success/?username={user.username}')
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

            otp_method = request.POST.get('otp_method')
            totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
            
            request.session['username'] = user.username
            request.session['otp_secret_key'] = totp.secret
            request.session['otp_valid_date'] = (datetime.now() + timedelta(minutes=1)).isoformat()
            print("----------------------------------")
            print("username: " + request.session['username'])
            print("otp_secret_key: " + request.session['otp_secret_key'])
            print("otp_valid_date: " + request.session['otp_valid_date'])

            token = generate_jwt(user)

            # Create an HTTP response object
            response = HttpResponse(status=302)  # 302 redirect to another page
            response['Location'] = '/player/otp/'

            # Set the JWT as a cookie
            response.set_cookie(
                'jwt',
                token,
                httponly=True,  # Prevent JavaScript access to the cookie
                secure=True,  # Use Secure flag to ensure it's only sent over HTTPS
                samesite='Lax'  # Prevent CSRF attacks
            )
            print("JWT cookie set:", response.cookies['jwt'].value)
            #user_token = decode_jwt(request.session['jwt_token'])
            #print(f"user id from token: {user_token}")   
            print("----------------------------------")

            if  otp_method == 'sms':
                contact = str(user.phone_number)
                print("contact: " + contact)
                send_otp(request, totp, contact, method='sms')
            elif otp_method == 'email':
                contact = user.email
                print("contact: " + contact)
                send_otp(request, totp, contact, method='email')
            return response
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

@csrf_exempt
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


                    #login(request, user)

                    #user_token = decode_jwt(request.session['jwt_token'])
                    #print(f"user id from token: {user_token}")   
                    #print("----------------------------------")
                    
                    # Clear the session data
                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']
                    del request.session['username']

                    # Redirect to the account page
                    return render(request, 'player/account.html', {'user': user})
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


#@login_required
def account_view(request):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        user = decode_jwt(token)
        print(f"user: {user}")
        if user:
            # User is authenticated
            #JsonResponse({'message': 'Access granted', 'user': user.username})
            return render(request, 'player/account.html', {'user': user})
        else:
            # Token is invalid or expired
            return HttpResponseForbidden('Invalid or expired token')
    
    return HttpResponseForbidden('Authentication required')
    
    #user = request.user
    #player = get_object_or_404(Player, username=user.username)
    #if request.method == 'POST':
    #    form = PhoneForm(request.POST, instance=player)
    #    if form.is_valid():
    # #       form.save()
     #       return redirect(f'/player/account/?username={user.username}')
    #    else:
    #        form = PhoneForm(instance=player)
#
    #return render(request, 'player/account.html', {'form': form})


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
        print("STATUS 200")
        return redirect('/player/login/')

    token_info = response.json()
    access_token = token_info.get('access_token')
    if not access_token:
        print("NOT ACCESS TOKEN !")
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


    if not username or not email:
        return redirect('/player/login/')

    user, created = Player.objects.get_or_create(
        username=username,
        defaults={'email': email}
    )

    return render(request, 'player/account.html', {'user': user})


def logout_view(request):
    response = redirect('/player/login/')
    token = request.COOKIES.get('jwt')
    if token:
        BlacklistedToken.objects.create(token=token)
        response.delete_cookie('jwt')
    return response



from django.http import HttpResponse

def some_view(request):
    token = request.COOKIES.get('jwt_token')
    if token:
        print(f"JWT Token from Cookie: {token}")
        return HttpResponse(f"Token: {token}")
    else:
        return HttpResponse("No JWT Token found in cookies")


from django.http import JsonResponse
from .jwt import decode_jwt

def verify_jwt(request):
    token = request.COOKIES.get('jwt')
    if not token:
        return JsonResponse({'valid': False, 'message': 'No token found'}, status=401)
    
    user = decode_jwt(token)
    if user:
        return JsonResponse({'valid': True, 'message': 'Token is valid'})
    else:
        return JsonResponse({'valid': False, 'message': 'Invalid or expired token'}, status=401)