from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Player(AbstractUser):
    phone_number = PhoneNumberField()
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, default='fallback.png')
    rank = models.IntegerField(default=1000)

    def __str__(self):
        return self.username