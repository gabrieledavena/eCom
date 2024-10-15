from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from checkout.models import Notification


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