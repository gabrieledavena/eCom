from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from account.models import Customer, Supplier
from store.models import Prodotto, Marca, Category
from django.contrib.auth import get_user_model

class ProductViewTest(TestCase):

    def setUp(self):
        """
        Configura un ambiente di test con un prodotto, un utente e altri prodotti.
        """
        # Crea una marca per il prodotto
        self.marca = Marca.objects.create(nome='Nike')
        self.category = Category.objects.create(nome='Nike')

        # Crea un utente e un prodotto associato
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.customer = Customer.objects.create(user=self.user)
        # Crea altri prodotti

        self.user2 = get_user_model().objects.create_user(username='testuser2', password='<PASSWORD>')
        self.supplier = Supplier.objects.create(user=self.user2, is_supplier=True)
        self.product1 = Prodotto.objects.create(
            nome="Product 1",
            supplier=self.supplier,
            is_sold=False,
            marca=self.marca,
            category=self.category,
            description="Product 1 description"
        )

        self.product2 = Prodotto.objects.create(
            nome="Product 2",
            is_sold=False,
            supplier=self.supplier,
            marca=self.marca,
            category=self.category,
            description="Product 2 description"
        )

        self.product3 = Prodotto.objects.create(
            nome="Product 3",
            is_sold=False,
            supplier=self.supplier,
            marca=self.marca,
            category=self.category,
            description="Product 3 description"
        )

        # URL per visualizzare il prodotto

    def test_product_view_renders_correct_template(self):
        """
        Testa che la vista del prodotto utilizzi il template corretto.
        """
        url = reverse('store:product', kwargs={'pk': self.product1.pk})

        response = self.client.get(url)
        self.assertTemplateUsed(response, 'store/product.html')

    def test_product_view_correct_context(self):
        """
        Testa che il contesto della vista contenga il prodotto, advices, user_likes, e user_advices.
        """
        url = reverse('store:product', kwargs={'pk': self.product1.pk})

        response = self.client.get(url)

        # Verifica che il prodotto nel contesto sia il prodotto corretto
        self.assertEqual(response.context['product'], self.product1)



    def test_product_view_404_if_product_not_found(self):
        """
        Testa che venga restituito un errore 404 se il prodotto non esiste.
        """
        url = reverse('store:product', kwargs={'pk': 999})  # id inesistente
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class HomeStoreViewTest(TestCase):

        # URL per la vista home_store

    def setUp(self):
            """
            Configura un ambiente di test con un prodotto, un utente e altri prodotti.
            """
            # Crea una marca per il prodotto
            self.marca = Marca.objects.create(nome='Nike')
            self.category = Category.objects.create(nome='Nike')

            # Crea un utente e un prodotto associato
            self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
            self.customer = Customer.objects.create(user=self.user)
            # Crea altri prodotti

            self.user2 = get_user_model().objects.create_user(username='testuser2', password='<PASSWORD>')
            self.supplier = Supplier.objects.create(user=self.user2, is_supplier=True)
            self.product1 = Prodotto.objects.create(
                nome="Product 1",
                supplier=self.supplier,
                is_sold=False,
                price=20,
                marca=self.marca,
                category=self.category,
                description="Product 1 description"
            )

            self.product2 = Prodotto.objects.create(
                nome="Product 2",
                is_sold=False,
                price=30,
                supplier=self.supplier,
                marca=self.marca,
                category=self.category,
                description="Product 2 description"
            )

            self.product3 = Prodotto.objects.create(
                nome="Product 3",
                is_sold=False,
                price=10,
                supplier=self.supplier,
                marca=self.marca,
                category=self.category,
                description="Product 3 description"
            )


    def test_home_store_renders_correct_template(self):
        """
        Verifica che la vista utilizzi il template corretto.
        """
        url_home = reverse('store:home_store')
        response = self.client.get(url_home)
        self.assertTemplateUsed(response, 'store/home_store.html')

    def test_home_store_products_ordered_by_price_asc(self):
        """
        Verifica che i prodotti vengano ordinati per prezzo crescente.
        """
        url_home = reverse('store:home_store')

        response = self.client.get(url_home, {'order_by': 'price_asc'})
        products = response.context['products']
        self.assertEqual(products[0], self.product3)  # Prezzo più basso
        self.assertEqual(products[1], self.product1)
        self.assertEqual(products[2], self.product2)  # Prezzo più alto

    def test_home_store_products_ordered_by_price_desc(self):
        """
        Verifica che i prodotti vengano ordinati per prezzo decrescente.
        """
        url_home = reverse('store:home_store')

        response = self.client.get(url_home, {'order_by': 'price_desc'})
        products = response.context['products']
        self.assertEqual(products[0], self.product2)  # Prezzo più alto
        self.assertEqual(products[1], self.product1)
        self.assertEqual(products[2], self.product3)  # Prezzo più basso

    def test_home_store_products_ordered_by_name_asc(self):
        """
        Verifica che i prodotti vengano ordinati per nome crescente (A-Z).
        """
        url_home = reverse('store:home_store')

        response = self.client.get(url_home, {'order_by': 'name_asc'})
        products = response.context['products']
        self.assertEqual(products[0], self.product1)  # Nome A-Z
        self.assertEqual(products[1], self.product2)
        self.assertEqual(products[2], self.product3)

    def test_home_store_products_ordered_by_name_desc(self):
        """
        Verifica che i prodotti vengano ordinati per nome decrescente (Z-A).
        """
        url_home = reverse('store:home_store')

        response = self.client.get(url_home, {'order_by': 'name_desc'})
        products = response.context['products']
        self.assertEqual(products[0], self.product3)  # Nome Z-A
        self.assertEqual(products[1], self.product2)
        self.assertEqual(products[2], self.product1)
