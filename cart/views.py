from django.shortcuts import render

# Create your views here.
def cart_page(request):
    return render(request, "cart/cart_page.html", {})

def cart_add(request):
    return
def cart_delete(request):
    return
def cart_update(request):
    return