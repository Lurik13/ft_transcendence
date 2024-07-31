from django.urls import path
from . import views

app_name = "player"

urlpatterns = [
    path('register/', views.register_view, name="register"),
    path('success/', views.success_view, name='success'),
    path('login/', views.login_view, name="login"),
    path('otp/', views.otp_view, name="otp"),
    path('display_qr/', views.display_qr_view, name="display_qr"),
    path('account/', views.account_view, name="account"),
    path('auth/42/callback/', views.auth_42_callback, name='auth_42_callback'),

]