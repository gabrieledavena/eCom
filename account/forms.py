from django import forms
from django.contrib.auth.models import User
from .models import Supplier, Customer
from django.contrib.auth.forms import UserChangeForm

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    is_supplier = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password']

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ['user']
        fields = ('email', 'nome', 'cognome', 'indirizzo')

class SupplierProfileForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = []

