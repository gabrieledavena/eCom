from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from account.models import Supplier, Customer
from checkout.models import Order
from reviews.models import Review
from store.models import Prodotto, Marca, Category
from django.contrib.auth import get_user_model


class DisplaySupplierViewTest(TestCase):
    def setUp(self):
        # Configura un cliente di test

        # Crea un utente e un fornitore
        self.user = User.objects.create_user(username="supplier_user", password="password123")
        self.supplier = Supplier.objects.create(user=self.user, is_supplier=True)

        marca = Marca.objects.create(nome='pro')
        category = Category.objects.create(nome='pro')

        # Crea alcuni prodotti
        self.product1 = Prodotto.objects.create(
            supplier=self.supplier,
            nome="Scarpa A",
            price=100.00,
            is_sold=False,
            marca=marca,
            category=category,
            description="Scarpa di alta qualità, perfetta per il tempo libero.",
            size=42
        )

        self.product2 = Prodotto.objects.create(
            supplier=self.supplier,
            nome="Scarpa B",
            price=200.00,
            is_sold=False,
            marca=marca,
            category=category,
            description="Scarpa elegante per occasioni speciali.",
            size=43
        )


        # Configura l'URL per la view
        self.url = reverse('account:displaySupplier', args=[self.supplier.id])

    def test_view_renders_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'account/displaySupplier.html')

    def test_products_are_ordered_by_price_asc(self):
        response = self.client.get(self.url, {'order_by': 'price_asc'})
        products = response.context['products']
        self.assertEqual(products[0],self.product1)  # Prezzo più basso

    def test_products_are_ordered_by_price_desc(self):
        response = self.client.get(self.url, {'order_by': 'price_desc'})
        products = response.context['products']
        self.assertEqual(products[0], self.product2)  # Prezzo più alto

    def test_products_are_ordered_by_name_asc(self):
        response = self.client.get(self.url, {'order_by': 'name_asc'})
        products = response.context['products']
        self.assertEqual(products[0], self.product1)  # Nome in ordine A-Z

    def test_products_are_ordered_by_name_desc(self):
        response = self.client.get(self.url, {'order_by': 'name_desc'})
        products = response.context['products']
        self.assertEqual(products[0], self.product2)  # Nome in ordine Z-A

    def test_redirect_if_supplier_does_not_exist(self):
        url = reverse('account:displaySupplier', args=[999])  # ID inesistente
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)  # Deve restituire 404


class UserRegistrationViewTest(TestCase):

    def test_register_valid_user(self):
        """
        Test che un utente venga correttamente creato con un modulo valido.
        """
        # Dati validi per il form
        data = {
            'username': 'newuser',
            'password': 'psicur340',
            'is_supplier': False,
        }

        # Invia una richiesta POST con i dati del form
        response = self.client.post(reverse('account:register'), data)

        # Verifica che la risposta sia una redirezione alla home dello store
        self.assertRedirects(response, reverse('store:home_store'))

        # Verifica che l'utente sia stato creato
        user = get_user_model().objects.get(username='newuser')
        self.assertTrue(user.check_password('psicur340'))

        # Verifica che non sia stato creato un fornitore
        self.assertFalse(Supplier.objects.filter(user=user).exists())
        self.assertTrue(Customer.objects.filter(user=user).exists())

    def test_register_supplier(self):
        """
        Test che un utente venga creato come fornitore se is_supplier è True.
        """
        data = {
            'username': 'supplieruser',
            'password': 'supplierpassword123',
            'is_supplier': True,
        }

        response = self.client.post(reverse('account:register'), data)

        self.assertRedirects(response, reverse('store:home_store'))

        # Verifica che l'utente sia stato creato
        user = get_user_model().objects.get(username='supplieruser')
        self.assertTrue(user.check_password('supplierpassword123'))

        # Verifica che l'utente sia un fornitore e che `is_staff` sia True
        self.assertTrue(Supplier.objects.filter(user=user).exists())
        self.assertTrue(user.is_staff)

    def test_register_invalid_password(self):
        """
        Test che l'invio di una password non valida ritorni un errore.
        """
        data = {
            'username': 'userwithinvalidpassword',
            'password': 'short',
            'is_supplier': False,
        }

        response = self.client.post(reverse('account:register'), data)

        # Verifica che la vista ritorni alla pagina di registrazione
        self.assertEqual(response.status_code, 200)

        # Verifica che ci sia un errore nel campo password
        user_form = response.context['user_form']
        self.assertFormError(user_form, 'password',
                             'This password is too short. It must contain at least 8 characters.')

    def test_register_without_password(self):
        """
        Test che l'invio di un modulo senza password ritorni un errore.
        """
        data = {
            'username': 'userwithoutpassword',
            'is_supplier': False,
        }

        response = self.client.post(reverse('account:register'), data)

        # Verifica che la vista ritorni alla pagina di registrazione
        self.assertEqual(response.status_code, 200)

        # Verifica che ci sia un errore nel campo password
        user_form = response.context['user_form']
        self.assertFormError(user_form, 'password', 'This field is required.')

class CustomerViewTests(TestCase):

    def setUp(self):
        """
        Crea un utente e un customer per i test.
        """
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password123',
        )
        self.customer = Customer.objects.create(
            user=self.user,
            nome='Mario',
            cognome='Rossi',
            email='mario.rossi@example.com',
            indirizzo='Via Roma 1',
        )
        self.user2 = get_user_model().objects.create_user(
            username='testsup',
            password='suppassword123',
        )
        self.supplier = Supplier.objects.create(user=self.user2, is_supplier=True)


    def test_customer_update_view(self):
        """
        Testa la vista di aggiornamento dei dati del customer.
        """
        self.client.login(username='testuser', password='password123')

        # URL per la vista di aggiornamento
        url = reverse('account:update_user', kwargs={'pk': self.customer.pk})

        # Dati del modulo per aggiornare l'utente
        data = {
            'nome': 'Giovanni',
            'cognome': 'Bianchi',
            'email': 'giovanni.bianchi@example.com',
            'indirizzo': 'Via Milano 2',
        }

        response = self.client.post(url, data)

        # Verifica che la risposta sia un redirect
        self.assertRedirects(response, reverse('store:home_store'))

        # Verifica che i dati siano stati aggiornati correttamente
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.nome, 'Giovanni')
        self.assertEqual(self.customer.cognome, 'Bianchi')
        self.assertEqual(self.customer.email, 'giovanni.bianchi@example.com')
        self.assertEqual(self.customer.indirizzo, 'Via Milano 2')

    def test_customer_profile_view(self):
        """
        Testa la vista del profilo del customer.
        """
        # Creazione di alcuni prodotti e ordini per il test
        self.client.login(username='testuser', password='password123')

        marca = Marca.objects.create(nome='pro')
        category = Category.objects.create(nome='pro')
        product = Prodotto.objects.create(nome='Product 1', is_sold=False, supplier=self.supplier, marca=marca, category=category)
        product.likes.add(self.customer)


        # URL per visualizzare il profilo del cliente
        url = reverse('account:customerprofile', kwargs={'pk': self.customer.pk})

        response = self.client.get(url)

        # Verifica che la risposta sia 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Verifica che il contesto contenga il customer e i prodotti piaciuti
        self.assertEqual(response.context['customer'], self.customer)
        self.assertEqual(
            list(response.context['liked_products'].values_list('nome', flat=True)),
            ['PRODUCT 1']
        )


class SupplierProfileViewTest(TestCase):

    def setUp(self):
        # Crea un utente e un fornitore
        self.user = get_user_model().objects.create_user(username='supplier_user', password='password123', is_staff=True)
        self.other_user = get_user_model().objects.create_user(username='other_user', password='password123')
        self.customer = Customer.objects.create(user=self.other_user)
        self.supplier = Supplier.objects.create(user=self.user, is_supplier=True)
        self.url = reverse('account:supplierprofile', kwargs={'pk': self.supplier.pk})

        # Crea prodotti associati al fornitore
        self.product1 = Prodotto.objects.create(nome='Product 1', supplier=self.supplier, is_sold=False, marca= Marca.objects.create(nome='test'), category= Category.objects.create(nome='test'))
        self.product2 = Prodotto.objects.create(nome='Product 2', supplier=self.supplier, is_sold=True,  marca= Marca.objects.create(nome='test'), category= Category.objects.create(nome='test'))

        self.order= Order.objects.create(customer=self.customer, supplier=self.supplier)
        self.order2= Order.objects.create(customer=self.customer, supplier=self.supplier)
        # Crea recensioni per il fornitore
        self.review1 = Review.objects.create(supplier=self.supplier, rating=4, comment='Good', customer=self.customer, order=self.order)
        self.review2 = Review.objects.create(supplier=self.supplier, rating=5, comment='Excellent', customer=self.customer, order=self.order2)

    def test_supplier_profile_view_authenticated(self):
        # Effettua il login come il fornitore
        self.client.login(username='supplier_user', password='password123')

        # Verifica che la vista restituisca lo stato 200
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # Verifica che i prodotti filtrati siano nel contesto
        self.assertIn('products', response.context)
        self.assertEqual(list(response.context['products']), [self.product1])  # Solo i prodotti non venduti

        # Verifica le recensioni
        self.assertIn('reviews', response.context)
        self.assertEqual(list(response.context['reviews']), [self.review1, self.review2])

        # Verifica il calcolo della media
        self.assertIn('average', response.context)
        self.assertEqual(response.context['average'], 4)  # Media delle recensioni (4.5 troncato a 4)
        self.assertEqual(response.context['halfstar'], 1)  # Mezza stella
        self.assertEqual(response.context['empty'], 0)  # Nessuna stella vuota

    def test_supplier_profile_view_unauthorized(self):
        # Effettua il login come un utente diverso
        self.client.login(username='other_user', password='password123')

        # Prova ad accedere al profilo di un altro fornitore
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('store:home_store'))

        # Verifica che il messaggio sia stato impostato
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Non hai il permesso di accedere a questo profilo")



class AddProductTest(TestCase):

    def setUp(self):
        # Crea un utente e un fornitore associato
        self.user = get_user_model().objects.create_user(username='supplier_user', password='password123', is_staff=True)
        self.other_user = User.objects.create_user(username='other_user', password='password123')
        self.supplier = Supplier.objects.create(user=self.user, is_supplier=True)
        self.url = reverse('account:addproduct')

        self.marca = Marca.objects.create(nome='Test Brand')
        self.category = Category.objects.create(nome='Test Category')
    def test_add_product_authenticated(self):
        # Effettua il login come il fornitore
        self.client.login(username='supplier_user', password='password123')

        # Crea i dati per un nuovo prodotto
        data = {
            'nome': 'New Product',
            'description': 'A wonderful new product',
            'price': 100.0,
            'size':40,
            'marca': self.marca.id,
            'category': self.category.id,
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('account:supplierprofile', kwargs={'pk': self.supplier.pk}))


        # Verifica che il prodotto sia stato salvato con il fornitore corretto
        product = Prodotto.objects.get(nome='NEW PRODUCT')
        self.assertEqual(product.supplier, self.supplier)  # Verifica che il fornitore sia quello giusto

    def test_add_product_invalid(self):
        # Effettua il login come il fornitore
        self.client.login(username='supplier_user', password='password123')

        # Dati non validi (manca il nome)
        data = {
            'nome': '',  # Campo nome vuoto (non valido)
            'price': 100.0,
            'size': 40,
            'marca': self.marca.id,
            'category': self.category.id,
        }

        response = self.client.post(self.url, data)

        # Verifica che la risposta contenga il form
        self.assertContains(response, '<form')


class DeleteProductTest(TestCase):

    def setUp(self):
        # Crea un utente e un fornitore associato
        self.user = get_user_model().objects.create_user(username='supplier_user', password='password123', is_staff=True)
        self.supplier = Supplier.objects.create(user=self.user, is_supplier=True)

        # Crea oggetti Marca e Category per il test
        self.marca = Marca.objects.create(nome='Test Brand')
        self.category = Category.objects.create(nome='Test Category')

        # Crea un prodotto da associare al fornitore
        self.product = Prodotto.objects.create(
            nome='Product to Delete',
            description='A product that will be deleted',
            price=100.0,
            size=40,
            marca=self.marca,
            category=self.category,
            supplier=self.supplier,
            is_sold=False,
        )

        # URL per eliminare il prodotto
        self.url = reverse('account:deleteproduct', kwargs={'pk': self.product.pk})

    def test_delete_product_authenticated_and_owner(self):
        # Effettua il login come il fornitore che possiede il prodotto
        self.client.login(username='supplier_user', password='password123')
        self.assertEqual(Prodotto.objects.filter(id=self.product.id).count(), 1)

        # Simula la richiesta di eliminazione (POST)
        response = self.client.post(self.url)

        # Verifica che il prodotto sia stato eliminato
        self.assertEqual(Prodotto.objects.filter(id=self.product.id).count(), 0)

        # Verifica che ci sia una redirezione
        self.assertRedirects(response, reverse('account:supplierprofile', kwargs={'pk': self.supplier.pk}))

    def test_delete_product_not_found(self):
        # Test che il prodotto non esiste più (usiamo un id che non esiste)
        self.client.login(username='supplier_user', password='password123')

        invalid_url = reverse('account:deleteproduct', kwargs={'pk': 999})

        # Simula la richiesta di eliminazione con un prodotto che non esiste
        response = self.client.post(invalid_url)

        # Verifica che venga restituito un errore 404 (Not Found)
        self.assertEqual(response.status_code, 404)