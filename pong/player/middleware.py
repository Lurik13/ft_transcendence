from django.shortcuts import redirect

class TwoFactorAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated and not request.user.is_2fa_verified:
            if not request.path.startswith('/player/tfa/'):
                return redirect('/player/tfa/')
        return response
