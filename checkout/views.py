from itertools import product
from pyexpat.errors import messages

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.utils import timezone
from account.models import Supplier
from cart.cart import Cart
from checkout.models import Notification, Order, OrderItem
from django.contrib import messages



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

@login_required
def checkout(request):
    if request.user.is_staff:
        messages.success(request, 'Devi essere un customer')
        return redirect('account:login')
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

@staff_member_required
def accept_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    for item in order.items.all():
        if (item.prodotto.is_sold):
            Notification.objects.create(recipient=order.customer.user, message=f"Impossibile continuare con l'ordine in quanto uno o più prodotti sono già stati venduti")
            reject_order(request, order_id)
        item.prodotto.is_sold=True
        item.prodotto.save()
        item.save()
    Notification.objects.create(recipient=request.user,message=f"Hai accettato l'ordine {order.id}")
    Notification.objects.create(recipient=order.customer.user,message=f"{order.supplier} ha accettato l'ordine {order.id}")
    order.status = "ACCEPTED"
    order.save()

    return redirect('checkout:supplierorderview')

@staff_member_required
def reject_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    Notification.objects.create(recipient=request.user,message=f"Hai rifiutato l'ordine {order.id}")
    Notification.objects.create(recipient=order.customer.user,message=f"{order.supplier} ha rifiutato l'ordine {order.id}")
    order.delete()

    return redirect('checkout:supplierorderview')

@staff_member_required
def ship_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = "TRANSITING"
    order.shipped_at = timezone.now()
    order.save()

    Notification.objects.create(recipient=request.user, message=f"Hai spedito l'ordine {order.id}")
    Notification.objects.create(recipient=order.customer.user,message=f"{order.supplier} ha spedito l'ordine {order.id}")

    return redirect('checkout:supplierorderview')


class SupplierOrderView(UserPassesTestMixin, TemplateView):
    template_name = "checkout/supplierOrderView.html"
    model = Supplier

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Recupera gli ordini dell'utente
        pending_orders = self.request.user.supplier.orders.filter(status='PENDING')
        accepted_orders = self.request.user.supplier.orders.filter(status='ACCEPTED')
        completed_orders = self.request.user.supplier.orders.filter(status='COMPLETED')
        transiting_orders = self.request.user.supplier.orders.filter(status='TRANSITING')

        # Aggiungi gli ordini al contesto con i relativi items
        context['pending_orders'] = pending_orders.prefetch_related('items')  # Usa prefetch_related
        context['accepted_orders'] = accepted_orders.prefetch_related('items')
        context['completed_orders'] = completed_orders.prefetch_related('items')
        context['transiting_orders'] = transiting_orders.prefetch_related('items')

        return context