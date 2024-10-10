from django import forms
from django.contrib.auth.models import User
from .models import Supplier

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    is_supplier = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password']

class SupplierProfileForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = []