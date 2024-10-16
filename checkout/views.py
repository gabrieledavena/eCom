from itertools import product

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from cart.cart import Cart
from checkout.models import Notification, Order, OrderItem


# Create your views here.
@login_required
def notification_list(request):
    notifications = request.user.notifications.all().order_by('-created_at')
    return render(request, 'checkout/notifications.html', {'notifications': notifications})


@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return redirect('checkout:notification_list')

def checkout(request):
    cart = Cart(request)
    suppliers = cart.get_suppliers()
    for supplier in suppliers:
        #Creo un ordine per ogni supplier
        order = Order.objects.create(customer=request.user.customer, supplier=supplier)
        for product in cart.get_items_by_supplier(supplier):
            #Creo un order item per ogni prodotto, che è legato a ordine conforeign key
            OrderItem.objects.create(order=order, prodotto=product)

        #Mando le notifiche a tutti
        Notification.objects.create(recipient=supplier.user, message=f"Offerta di acquisto da {request.user.username}, ordine {order.id}")
        Notification.objects.create(recipient=request.user, message=f"Offerta di acquisto inviata a {supplier.user.username}, ordine {order.id}")

    #cancello il carrello
    cart.clear()
    return redirect('store:home_store')