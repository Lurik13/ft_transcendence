from django.urls import path
from . import views
from . import jwt

app_name = "player"

urlpatterns = [
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('otp/', views.otp_view, name="otp"),
    path('account/', views.account_view, name="account"),
    path('auth/42/callback/', views.auth_42_callback, name='auth_42_callback'),
    path('logout/', views.logout_view, name='logout'),
    path('verify-jwt/', jwt.verify_jwt, name='verify_jwt'),
    path('toggle_2fa/', views.toggle_2fa, name='toggle_2fa'),
    path('update/', views.update, name='update'),
    path('update/password', views.update_password, name='update_password'),
]