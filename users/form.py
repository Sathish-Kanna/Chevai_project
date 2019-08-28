from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from .models import Profile, Service


class UserRegisterForm(UserCreationForm):
    username = forms.EmailField(max_length=100, required=True, label='E-mail')
    name = forms.CharField(max_length=100, required=True)
    phone_regex = RegexValidator(regex=r'^\+?\d{10,12}$',
                                 message='Phone number must be entered in the format: "+919876543210"')
    phone_number = forms.CharField(validators=[phone_regex], min_length=12, max_length=14, required=True)

    class Meta:
        model = User
        fields = ['name', 'username', 'password1', 'password2', 'phone_number']


class ProfileUpdateForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True)
    phone_regex = RegexValidator(regex=r'^\+?\d{10,12}$',
                                 message='Phone number must be entered in the format: "+919876543210"')
    phone_number = forms.CharField(validators=[phone_regex], min_length=12, max_length=14, required=True)
    language = forms.CharField(max_length=100, required=True)
    location = forms.CharField(widget=forms.Textarea, required=True)
    pin_regex = RegexValidator(regex=r'\d{5,7}$',
                               message='Pin number must be entered in the format: "605001"')
    pin = forms.CharField(validators=[pin_regex], min_length=5, max_length=7, required=True)
    # image = forms.ImageField(required=True)

    class Meta:
        model = Profile
        fields = ['name', 'phone_number', 'language', 'location', 'pin', 'image']


class UserServiceForm(forms.ModelForm):
    skill = forms.CharField(max_length=50, required=True)
    price = forms.IntegerField(min_value=0)

    class Meta:
        model = Service
        fields = ['skill', 'price']
