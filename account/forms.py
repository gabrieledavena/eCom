from django import forms
from django.contrib.auth.models import User

from store.models import Prodotto
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

class ProductForm(forms.ModelForm):
    class Meta:
        model = Prodotto
        fields = ['nome', 'price', 'image', 'category', 'description', 'size', 'marca']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',  # Fallback styling (for non-template tweaks users)
            }),
        }

class PasswordResetForm(forms.Form):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    new_password = forms.CharField(
        label="Nuova Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    confirm_password = forms.CharField(
        label="Conferma Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Le password non corrispondono.")
        return cleaned_data
