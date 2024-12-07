from django.shortcuts import render
from django.db.models import Avg
from account.models import Supplier


def home_page(request):
    suppliers = Supplier.objects.annotate(average_rating=Avg('reviews__rating')).order_by('-average_rating')[:5]

    return render(request, 'home.html', {'suppliers': suppliers})

