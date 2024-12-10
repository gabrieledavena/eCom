from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
# tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from account.models import Customer
from store.models import Prodotto, Marca, Category
from .models import Order, Review, Supplier

class CreateReviewTest(TestCase):
    def setUp(self):
        # Create a customer and supplier user for testing
        self.customer_user = get_user_model().objects.create_user(username='customeruser', password='password', is_staff=False)
        self.supplier_user = get_user_model().objects.create_user(username='supplieruser', password='password', is_staff=True)

        # Create a product and an order
        self.supplier = Supplier.objects.create(user=self.supplier_user)
        self.customer = Customer.objects.create(user=self.customer_user)
        self.marca = Marca.objects.create(nome='MarcaTest')
        self.category = Category.objects.create(nome='CategoriaTest')

        self.product = Prodotto.objects.create(nome="Test Product", price=100, supplier=self.supplier, marca=self.marca, category=self.category)
        self.order = Order.objects.create(customer=self.customer_user.customer, supplier=self.supplier, status='TRANSITING')

        # Log in as the customer
        self.client.login(username='customeruser', password='password')

    def test_create_review_post_valid(self):
        # Prepare the data for the review
        data = {
            'rating': 5,
            'comment': 'Great product, very satisfied!'
        }

        # Send the POST request to create the review
        response = self.client.post(reverse('reviews:create_review', args=[self.order.id]), data)

        # Check if the review was saved
        review = Review.objects.first()
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'Great product, very satisfied!')
        self.assertEqual(review.order, self.order)
        self.assertEqual(review.customer, self.customer_user.customer)
        self.assertEqual(review.supplier, self.supplier)

        # Check that the order's status is updated to 'COMPLETED'
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'COMPLETED')

        # Check that the user is redirected to the home page
        self.assertRedirects(response, reverse('store:home_store'))

    def test_create_review_get(self):
        # Send a GET request to render the review form
        response = self.client.get(reverse('reviews:create_review', args=[self.order.id]))

        # Check that the response is successful and the correct template is used
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/create_review.html')

        # Ensure that the form is in the context
        self.assertIn('form', response.context)
