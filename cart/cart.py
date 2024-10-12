from itertools import product

from store.models import Prodotto





class Cart():
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get('session_key')

        #Nuovo user -> no key
        if'session_key' not in request.session:
            cart = self.session['session_key']={}


        self.cart = cart
    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.cart:
            # È come un dizionario
            self.cart[product_id] = {'price': str(product.price)}

        self.session.modified = True

    #Per aggiornare il numero del carrello
    def __len__(self):
        return len(self.cart)

    def get_products(self):
        product_ids = self.cart.keys()

        #Li cerco nel database
        products = Prodotto.objects.filter(id__in=product_ids)
        return products

    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True


    def total(self):
        total = 0
        for product in self.get_products():
            total += product.price
        self.session.modified = True
        return total