from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Halisaha

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class HalisahaForm(forms.ModelForm):
    class Meta:
        model = Halisaha
        fields = ['name', 'address', 'phone', 'hourly_price', 'location_url']