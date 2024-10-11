from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm
from .models import Supplier 
from store.models import Customer
# Create your views here.

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            # Controlla se l'utente è un fornitore
            is_supplier = user_form.cleaned_data['is_supplier']
            if is_supplier:
                user.is_staff=True
                user.save()
                
                Supplier.objects.create(user=user, is_supplier=True)
            else:
                Customer.objects.create(user=user)
            login(request, user)

            return redirect('store:home_store')
    else:
        user_form = UserRegistrationForm()

    return render(request, 'account/register.html', {'user_form': user_form})