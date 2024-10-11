from django.shortcuts import render, get_object_or_404
from .models import Prodotto

# Create your views here.

def product_view(request, pk):
    product = get_object_or_404(Prodotto, id=pk)
    return render(request, "store/product.html", {'product':product})

def home_store(request):
    products=Prodotto.objects.all()
    return render(request, "store/home_store.html", {'products':products})
