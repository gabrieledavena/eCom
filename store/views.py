from django.contrib.auth.decorators import login_not_required
from django.shortcuts import redirect, get_object_or_404, render
from .models import Prodotto, Category

# Create your views here.

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
    products=Prodotto.objects.all().filter(is_sold=False)
    if request.user.is_authenticated:
        unread_notifications_count = request.user.notifications.filter(is_read=False).count()
    else:
        unread_notifications_count = 0

    return render(request, "store/home_store.html", {'products':products, 'unread_notifications_count': unread_notifications_count})

