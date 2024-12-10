from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse

from account.models import Customer, Supplier
from cart.cart import Cart
from checkout.models import Notification, Order, OrderItem
from store.models import Prodotto, Marca, Category


# Create your tests here.

class NotificationListViewTest(TestCase):
    def setUp(self):
        # Create a user and log them in
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.customer = Customer.objects.create(user=self.user)

        # Create some notifications for the user
        Notification.objects.create(recipient=self.user, message="Test Notification 1", is_read=False)
        Notification.objects.create(recipient=self.user, message="Test Notification 2", is_read=False)

        # Create another user with no notifications
        self.other_user = get_user_model().objects.create_user(username='otheruser', password='password')
        self.othercustomer = Customer.objects.create(user=self.other_user)

    def test_notification_list_view(self):
        # Log in the user
        self.client.login(username='testuser', password='password')

        # Get the notification list view
        response = self.client.get(reverse('checkout:notification_list'))

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Check if the notifications appear in the context
        self.assertIn('notifications', response.context)

        # Check that the notifications are rendered in the template
        self.assertContains(response, "Test Notification 1")
        self.assertContains(response, "Test Notification 2")

    def test_no_notifications_for_other_user(self):
        # Log in as the other user who has no notifications
        self.client.login(username='otheruser', password='password')

        # Get the notification list view
        response = self.client.get(reverse('checkout:notification_list'))

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Check that the context has no notifications
        self.assertIn('notifications', response.context)
        self.assertEqual(len(response.context['notifications']), 0)


class SupplierOrderViewTest(TestCase):
    def setUp(self):
        # Create a staff user and a non-staff user
        self.staff_user = get_user_model().objects.create_user(username='staffuser', password='password', is_staff=True)

        # Create a supplier for the users
        self.supplier = Supplier.objects.create(user=self.staff_user, is_supplier=True)

        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.customer = Customer.objects.create(user=self.user)


        # Create some orders for the supplier
        self.order1 = Order.objects.create(supplier=self.supplier, status="PENDING", customer=self.customer)
        self.order2 = Order.objects.create(supplier=self.supplier, status="ACCEPTED", customer=self.customer)
        self.order3 = Order.objects.create(supplier=self.supplier, status="COMPLETED", customer=self.customer)
        self.order4 = Order.objects.create(supplier=self.supplier, status="TRANSITING", customer=self.customer)


    def test_staff_user_can_access_view(self):
        # Log in as a staff user and check access
        self.client.login(username='staffuser', password='password')
        response = self.client.get(reverse('checkout:supplierorderview'))  # Update with your actual URL name
        self.assertEqual(response.status_code, 200)  # Should be successful for staff user

    def test_non_staff_user_cannot_access_view(self):
        # Log in as a non-staff user and check access
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('checkout:supplierorderview'))  # Update with your actual URL name
        self.assertEqual(response.status_code, 403)  # Should be forbidden for non-staff user

    def test_correct_orders_in_context_for_staff(self):
        # Log in as a staff user
        self.client.login(username='staffuser', password='password')

        # Get the supplier order view
        response = self.client.get(reverse('checkout:supplierorderview'))  # Update with your actual URL name

        # Check that orders with the correct status are in the context
        self.assertIn('pending_orders', response.context)
        self.assertIn('accepted_orders', response.context)
        self.assertIn('completed_orders', response.context)
        self.assertIn('transiting_orders', response.context)

        # Check the order count in the context
        self.assertEqual(response.context['pending_orders'].count(), 1)
        self.assertEqual(response.context['accepted_orders'].count(), 1)
        self.assertEqual(response.context['completed_orders'].count(), 1)
        self.assertEqual(response.context['transiting_orders'].count(), 1)


class CheckoutViewTest(TestCase):
    def setUp(self):
        # Create a staff user and a non-staff user
        self.staff_user = get_user_model().objects.create_user(username='staffuser', password='password', is_staff=True)
        self.customer_user = get_user_model().objects.create_user(username='customeruser', password='password', is_staff=False)

        # Create a product and a supplier for testing
        self.supplier = Supplier.objects.create(user=self.staff_user, is_supplier=True)
        self.customer = Customer.objects.create(user=self.customer_user)
        self.marca = Marca.objects.create(nome='MarcaTest')
        self.category = Category.objects.create(nome='CategoriaTest')

        self.product = Prodotto.objects.create(nome="Test Product", price=100, supplier=self.supplier, marca=self.marca, category=self.category, is_sold=False, size=40)

        self.client.login(username='customeruser', password='password')


    def test_checkout_for_customer(self):
        # Log in as a customer (non-staff user)
        self.client.login(username='customer_user', password='passicur123')
        # Esegui una richiesta POST con i dati necessari
        self.url = reverse('cart:cart_add')
        response = self.client.post(
            self.url,
            data={'action': 'post', 'product_id': self.product.id}
        )
        cart = Cart(self.client)
        self.assertEqual(cart.__len__(), 1)
        self.assertEqual(len(cart.get_products()), 1)

        # Get the checkout view
        response = self.client.get(reverse('checkout:checkout'))

        # Check that the response is successful (status code 302 redirects)
        self.assertEqual(response.status_code, 302)


       # Check that orders and order items were created
        orders = Order.objects.filter(customer=self.customer)
        self.assertEqual(orders.count(), 1)  # 1 order

        order = orders.first()
        order_items = OrderItem.objects.filter(order=order)
        self.assertEqual(order_items.count(), 1)  # 1 order item

        # Check notifications
        notifications = Notification.objects.filter(recipient=self.customer_user)
        self.assertEqual(notifications.count(), 1)  # 1 notification for customer

        notifications = Notification.objects.filter(recipient=self.staff_user)
        self.assertEqual(notifications.count(), 1)  # 1 notification for  supplier

