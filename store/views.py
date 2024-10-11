from django.shortcuts import render
from .models import Prodotto

# Create your views here.
def home_store(request):
    products=Prodotto.objects.all()
    return render(request, "store/home_store.html", {'products':products})