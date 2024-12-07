from itertools import product

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import request

#Per il carrello
from .cart import Cart
from store.models import Prodotto
from django.http import JsonResponse

#Per i messaggi
from django.contrib import messages


# Create your views here.
@login_required
def cart_page(request):
    if request.user.is_staff:
        messages.error(request, 'Accesso negato: non hai i permessi necessari per accedere a questa pagina.')
        return redirect('store:home_store')
    else:
        cart = Cart(request)
        products = cart.get_products()
        totals = cart.total()
        return render(request, "cart/cart_page.html", {'products': products, 'totals': totals})

@login_required
def cart_add(request):
    if request.user.is_staff:
        messages.error(request, 'Accesso negato: non hai i permessi necessari per accedere a questa pagina.')
        return redirect('store:home_store')
    else:
        cart = Cart(request)
        #testo per POST
        if request.POST.get('action') == 'post':
            product_id = int(request.POST.get('product_id'))
            product = get_object_or_404(Prodotto, id=product_id)
            carr_vecchio = cart.__len__()
            cart.add(product=product)

            cart_quantity = cart.__len__()
            response = JsonResponse({'quantity': cart_quantity})
            if carr_vecchio == cart.__len__():
                messages.success(request, ("Prodotto già presente nel carrello"))
            else:
                messages.success(request, ("Prodotto aggiunto al carrello"))
            return response


@login_required
def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product = product_id)

        response = JsonResponse({'product': product_id})
        messages.success(request, ("Prodotto tolto dal carrello"))

        return response
