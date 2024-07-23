from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Player

@admin.register(Player)
class Player_admin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile_picture', 'rank', 'phone_number')}),
    )