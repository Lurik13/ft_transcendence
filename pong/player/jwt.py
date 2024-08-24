import jwt
import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import BlacklistedToken, Player
from django.http import JsonResponse

User = get_user_model()

def generate_jwt(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.JWT_EXP_DELTA_SECONDS),
        'iat': datetime.datetime.utcnow(),
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token

def decode_jwt(token):
    if BlacklistedToken.objects.filter(token=token).exists():
        return None  # Token is blacklisted
    # Otherwise, decode as usual
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
        return Player.objects.get(id=payload['user_id'])
    except (jwt.ExpiredSignatureError, jwt.DecodeError, Player.DoesNotExist):
        return None

def verify_jwt(request):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        payload = decode_jwt(token)
        if payload:
            return JsonResponse({'valid': True})
    return JsonResponse({'valid': False}, status=401)