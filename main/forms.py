from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Halisaha


from .models import Reservation


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class HalisahaForm(forms.ModelForm):
    class Meta:
        model = Halisaha
        fields = ['name', 'address', 'phone', 'hourly_price', 'location_url']


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date', 'hour_range']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'hour_range': forms.TextInput(attrs={'placeholder': 'Örn: 14:00 - 15:00'}),
        }
