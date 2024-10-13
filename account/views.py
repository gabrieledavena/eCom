from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm, CustomerProfileForm
from .models import Supplier 
from store.models import Customer, User, Prodotto
# Create your views here.
from django.contrib import messages
from django.views.generic import UpdateView, DetailView


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

class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerProfileForm
    template_name = 'account/update_user.html'

    def get_success_url(self):
        pk = self.get_context_data()["object"].pk
        return reverse('store:home_store')

class CustomerProfileView(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = 'account/customerprofile.html'

class SupplierProfileView(LoginRequiredMixin, DetailView):
    model = Supplier
    template_name = 'account/supplierprofile.html'

    context_object_name = 'supplier'  # Per riferirsi al fornitore nel template

    # Sovrascrivi il metodo per aggiungere i prodotti al contesto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ottieni tutti i prodotti associati al fornitore corrente
        context['products'] = Prodotto.objects.filter(supplier=self.object)
        return context