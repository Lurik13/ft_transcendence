# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumbers.phonenumberutil import is_valid_number, parse
from .models import Player

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label='Email Address',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    phone_number = forms.CharField(
        label='Phone Number',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        try:
            parsed_number = parse(phone_number, None)
            if not is_valid_number(parsed_number):
                raise forms.ValidationError("Invalid phone number")
        except Exception as e:
            raise forms.ValidationError("Invalid phone number")
        return phone_number

    def save(self, commit=True):
        user = super().save(commit=commit)
        user_profile = Player.objects.create(user=user, phone_number=self.cleaned_data['phone_number'])
        if commit:
            user_profile.save()
        return user
