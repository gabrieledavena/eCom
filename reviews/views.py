from django.shortcuts import render, get_object_or_404, redirect

from checkout.models import Order
from reviews.forms import ReviewForm


# Create your views here.
def create_review(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.order = order
            review.customer = request.user.customer
            review.supplier = order.supplier
            review.save()
            order.status='COMPLETED'
            order.save()
            return redirect("store:home_store")
    else:
        form = ReviewForm()
    return render(request, "reviews/create_review.html", {"form": form, "order": order})