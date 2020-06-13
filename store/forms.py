from django import forms 
from .models import Customer, ShippingAddress
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = '__all__'

class CustomerRegisterForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username','email','password1','password2']

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user','username']