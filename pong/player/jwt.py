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
        return {'error': 'Token is blacklisted'}
    
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
        user = Player.objects.get(id=payload['user_id'])
        return user
    except jwt.ExpiredSignatureError:
        return {'error': 'Token has expired'}
    except jwt.DecodeError:
        return {'error': 'Token is invalid'}
    except Player.DoesNotExist:
        return {'error': 'User not found'}


def verify_jwt(request):
    token = request.COOKIES.get('jwt')
    if not token:
        return JsonResponse({'valid': False, 'message': 'No token found'}, status=401)
    
    user = decode_jwt(token)
    if user:
        print(f"user: {user}")
        return JsonResponse({'valid': True, 'message': 'Token is valid'})
    else:
        return JsonResponse({'valid': False, 'message': 'Invalid or expired token'}, status=401)