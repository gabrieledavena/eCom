from django.contrib.auth.decorators import login_not_required
from django.shortcuts import redirect, get_object_or_404, render
from .models import Prodotto, Category

# Create your views here.

def search(request):
    query = request.GET.get('query', '')
    if not query == '':
        products = Prodotto.objects.filter(nome__icontains=query).filter(is_sold= False) if query else []
    else:
        products = Prodotto.objects.filter(is_sold= False)
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')

    # Applica i Filtri se Specificati
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)
    return render(request, 'search_results.html', {'products': products, 'filters': {
            'price_min': price_min,
            'price_max': price_max,
        },
    })

def product_view(request, pk):
    product = get_object_or_404(Prodotto, id=pk)
    return render(request, "store/product.html", {'product':product})

def category(request, cat):
    try:
        myCategory = Category.objects.get(id=cat)
        products = Prodotto.objects.filter(category = myCategory)
    except:
        return redirect('/store')
    return render(request, 'store/category.html', {'products':products, 'category':myCategory})

def home_store(request):
    order_by = request.GET.get('order_by', 'price_asc')

    # Ordina i prodotti in base alla selezione
    if order_by == 'price_asc':
        products = Prodotto.objects.filter(is_sold=False).order_by(
            'price')  # Prezzo crescente
    elif order_by == 'price_desc':
        products = Prodotto.objects.filter(is_sold=False).order_by(
            '-price')  # Prezzo decrescente
    elif order_by == 'name_asc':
        products = Prodotto.objects.filter(is_sold=False).order_by('nome')  # Nome A-Z
    elif order_by == 'name_desc':
        products = Prodotto.objects.filter(is_sold=False).order_by('-nome')  # Nome Z-A
    else:
        products = Prodotto.objects.filter(is_sold=False)  # Default
    if request.user.is_authenticated:
        unread_notifications_count = request.user.notifications.filter(is_read=False).count()
    else:
        unread_notifications_count = 0

    return render(request, "store/home_store.html", {'products':products, 'unread_notifications_count': unread_notifications_count})

