from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Player(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, default='fallback.png')
    rank = models.IntegerField(default=1000)
    phone_number = PhoneNumberField(blank=True, null=True)

    def __str__(self):
        return self.username
    



