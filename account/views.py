
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.utils.functional import empty

from checkout.models import Order
from reviews.models import Review
from .forms import UserRegistrationForm, CustomerProfileForm, ProductForm
from .models import Supplier 
from store.models import Customer, Prodotto
# Create your views here.
from django.contrib import messages
from django.views.generic import UpdateView, DetailView, TemplateView


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

class CustomerProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/customerprofile.html'
    context_object_name = 'customer'  # Per riferirsi al utente nel template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer']= self.request.user.customer
        context['liked_products']=Prodotto.objects.filter(likes = self.request.user.customer).filter(is_sold=False)
        transiting_orders = self.request.user.customer.orders.filter(status="TRANSITING")
        context['transiting_orders'] = transiting_orders.prefetch_related('items')

        return context

    #Dato che sto usando una template view non bisogno del dispatch per capire se il customer che sta cercando di accedere è lo stesso del profilo, dato che lo passo nel contesto

class SupplierProfileView(LoginRequiredMixin, DetailView):
    model = Supplier
    template_name = 'account/supplierprofile.html'

    context_object_name = 'supplier'  # Per riferirsi al fornitore nel template

    # Sovrascrivi il metodo per aggiungere i prodotti al contesto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ottieni tutti i prodotti associati al fornitore corrente
        context['products'] = Prodotto.objects.filter(supplier=self.object).filter(is_sold=False)
        context['reviews'] =Review.objects.filter(supplier=self.object)

        # Per la media stelle
        average=0
        for review in Review.objects.filter(supplier=self.object):
            average= average + review.rating
        if (len(Review.objects.filter(supplier=self.object))) > 0:
            average = average/len(Review.objects.filter(supplier=self.object))
            halfstar=0
            context['average'] = int (average)
            if average % 1 >= 0.3 :
                halfstar = 1
                context['halfstar'] = halfstar
            context['empty']= 5 -halfstar - int (average)
        else:
            context['empty'] = 5
            context['halfstar'] = 0
            context['average'] = 0

        return context

    def dispatch(self, request, *args, **kwargs):
        # Controlla se l'utente loggato è lo stesso associato al profilo del fornitore
        supplier = self.get_object()  # Ottieni l'istanza del fornitore
        if request.user != supplier.user:  # ForeignKey User in Supplier
            messages.success(request,"Non hai il permesso di accedere a questo profilo")
            return redirect('store:home_store')
        return super().dispatch(request, *args, **kwargs)

def addproduct(request):  # Assicurati che sia 'supplier_id'
    # Cerca il fornitore con il supplier_id e verificane la proprietà

    supplier = Supplier.objects.get(user=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.supplier = supplier  # Associa il prodotto al fornitore
            product.save()
            messages.success(request, "Prodotto aggiunto con successo!")
            return redirect('account:supplierprofile', pk=supplier.pk)  # Reindirizza al profilo fornitore
    else:
        form = ProductForm()

    return render(request, 'account/add_product.html', {'form': form, 'supplier': supplier})

def delete_product(request, pk):
    product = get_object_or_404(Prodotto, id=pk)
    print(f"Attempting to delete product: {product.nome}")

    if request.method == 'POST':
        product.delete()
        messages.success(request, "Prodotto eliminato con successo!")
        return redirect('account:supplierprofile', pk=product.supplier.id)  # Reindirizza alla pagina del fornitore
    return redirect('account:supplierprofile', pk=product.supplier.id)  # Reindirizza alla pagina del fornitore

@login_required
def like(request, pk):
    if not request.user.is_staff:
        prodotto = get_object_or_404(Prodotto, id=pk)

        # Controlla se l'utente ha già messo il like
        if request.user.customer in prodotto.likes.all():
            # Rimuove il like se già presente
            prodotto.likes.remove(request.user.customer)
        else:
            # Aggiunge il like
            prodotto.likes.add(request.user.customer)

    return redirect('store:product', pk=pk)

def displaySupplier(request, pk):
    supplier = get_object_or_404(Supplier, id=pk)

    order_by = request.GET.get('order_by', 'price_asc')

    # Ordina i prodotti in base alla selezione
    if order_by == 'price_asc':
        products = Prodotto.objects.filter(supplier=supplier).filter(is_sold=False).order_by('price')  # Prezzo crescente
    elif order_by == 'price_desc':
        products = Prodotto.objects.filter(supplier=supplier).filter(is_sold=False).order_by('-price')  # Prezzo decrescente
    elif order_by == 'name_asc':
        products = Prodotto.objects.filter(supplier=supplier).filter(is_sold=False).order_by('nome')  # Nome A-Z
    elif order_by == 'name_desc':
        products = Prodotto.objects.filter(supplier=supplier).filter(is_sold=False).order_by('-nome')  # Nome Z-A
    else:
        products = Prodotto.objects.filter(supplier=supplier).filter(is_sold=False)  # Default
    reviews = Review.objects.filter(supplier=supplier)

    average = 0
    for review in Review.objects.filter(supplier=supplier):
        average = average + review.rating
    if (len(Review.objects.filter(supplier=supplier))) > 0:
        average = average / len(Review.objects.filter(supplier=supplier))
        halfstar = 0
        if average % 1 >= 0.3:
            halfstar = 1
        empty = 5-halfstar - int (average)
    else:
        average = 0
        halfstar = 0
        empty=5
    return render(request, 'account/displaySupplier.html', {'products': products, 'supplier': supplier, 'reviews': reviews, 'average': average, 'halfstar': halfstar, 'empty': empty})