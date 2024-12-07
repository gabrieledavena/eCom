from django.shortcuts import render

from account.models import Supplier


def home_page(request):
    Supplier.objects.all().order_by()
    return render(request, 'home.html')

