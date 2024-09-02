from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Player(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, default='profile_pictures/fallback.png')
    rank = models.IntegerField(default=1000)
    phone_number = PhoneNumberField(blank=True, null=True)

    def __str__(self):
        return self.username
    

class BlacklistedToken(models.Model):
    token = models.CharField(max_length=500)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token
