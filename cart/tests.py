import json
from multiprocessing.connection import Client

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest
from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client

from account.forms import UserRegistrationForm
from account.models import Customer, Supplier
from store.models import Prodotto, Marca, Category
from cart.cart import Cart  # Assumendo che la classe `Cart` sia definita in `cart/cart.py`.

client = Client()

class CartPageViewTest(TestCase):
    def setUp(self):

        # Creazione di un utente staff
        self.user = get_user_model().objects.create_user(username='supplier_user', password='supplier_password123', is_staff=True)
        self.supplier = Supplier.objects.create(user=self.user, is_supplier=True)

        self.url = reverse('cart:cart_page')

    def test_cart_access_for_staff_user(self):
        """
        Test che un utente staff non possa accedere alla pagina del carrello.
        """
        self.assertTrue(self.client.login(username='supplier_user', password='supplier_password123'))
        response = self.client.get(self.url)

        self.assertRedirects(response, reverse('store:home_store'))

    def test_cart_access_for_customer(self):
        """
        Test che un customer possa accedere alla pagina del carrello.
        """
        # Creazione di un utente cliente
        self.user2 = get_user_model().objects.create_user(username='customer_user', password='customer_password123')
        self.customer = Customer.objects.create(user=self.user2, nome="Customer", cognome="User")

        login_successful = self.client.login(username='customer_user', password='customer_password123')

        # Verifica che il login sia andato a buon fine
        self.assertTrue(login_successful)

        # Ora l'utente può accedere al carrello
        response = self.client.get(reverse('cart:cart_page'))
        self.assertEqual(response.status_code, 200)

    def test_cart_page_requires_login(self):
        """
        Test che la vista richieda che l'utente sia autenticato.
        """
        response = self.client.get(self.url)

        # Verifica che l'utente venga reindirizzato alla pagina di login
        self.assertRedirects(response,  '/account/login/?auth=notok&next=/cart/')



class CartAddViewTest(TestCase):
    def setUp(self):
        # Crea un utente customer
        self.customer_user = get_user_model().objects.create_user(
            username='customer_user', password='passicur123'
        )
        self.customer = Customer.objects.create(user=self.customer_user)

        # Crea un utente staff
        self.staff_user = get_user_model().objects.create_user(
            username='staff_user', password='password123', is_staff=True
        )
        self.supplier= Supplier.objects.create(user=self.staff_user, is_supplier=True)

        # Crea una marca e una categoria per i prodotti
        self.marca = Marca.objects.create(nome='MarcaTest')
        self.category = Category.objects.create(nome='CategoriaTest')


        # Crea un prodotto
        self.product = Prodotto.objects.create(
            nome='TestProduct',
            price=100.0,
            is_sold=False,
            marca=self.marca,
            category=self.category,
            supplier=self.supplier,
        )

        self.url = reverse('cart:cart_add')

    def test_cart_add_by_customer(self):
        """
        Test che un utente customer possa aggiungere un prodotto al carrello.
        """
        self.client.login(username='customer_user', password='passicur123')

        # Esegui una richiesta POST con i dati necessari

        response = self.client.post(
            self.url,
            data={'action': 'post', 'product_id': self.product.id}
        )
        self.assertEqual(response['Content-Type'], 'application/json')

        response_data = response.json()
        self.assertEqual(response_data['quantity'], 1)  # Assumendo che il carrello abbia 1 prodotto

        # Verifica che il prodotto sia stato aggiunto correttamente al carrello
        cart = Cart(self.client)
        self.assertEqual(cart.__len__(), 1)
        self.assertIn(str(self.product.id), cart.cart)


class CartDeleteTest(TestCase):
    def setUp(self):
        # Crea un prodotto per i test
        self.staff_user = get_user_model().objects.create_user(
            username='staff_user', password='password123', is_staff=True
        )
        self.supplier = Supplier.objects.create(user=self.staff_user, is_supplier=True)

        # Crea una marca e una categoria per i prodotti
        self.marca = Marca.objects.create(nome='MarcaTest')
        self.category = Category.objects.create(nome='CategoriaTest')

        # Crea un prodotto
        self.product = Prodotto.objects.create(
            nome='TestProduct',
            price=100.0,
            is_sold=False,
            marca=self.marca,
            category=self.category,
            supplier=self.supplier,
        )

        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

        # URL della view da testare
        self.url = reverse('cart:cart_delete')

        # Aggiungi il prodotto al carrello per i test
        request = HttpRequest()
        request.user = self.user
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        self.cart = Cart(request)
        self.cart.add(product=self.product)
        request.session.save()


def test_cart_delete_product(self):
        """
        Test che verifica la rimozione di un prodotto dal carrello.
        """
        # Verifica che il prodotto sia inizialmente nel carrello
        self.assertEqual(self.cart.__len__(), 1)

        # Simula una richiesta POST per rimuovere il prodotto
        response = self.client.post(
            self.url,
            data={'action': 'post', 'product_id': self.product.id}
        )

        # Verifica che il codice di risposta sia 200
        self.assertEqual(response.status_code, 200)

        # Controlla che la risposta sia JSON e contenga il product_id
        response_data = response.json()
        self.assertIn('product', response_data)
        self.assertEqual(response_data['product'], self.product.id)

        # Verifica che il prodotto sia stato rimosso dal carrello
        self.assertEqual(self.cart.__len__(), 0)

