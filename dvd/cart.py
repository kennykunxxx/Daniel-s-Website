from .models import Dvd, Order
from decimal import Decimal
from movie.models import movie

class Cart(object):
    
    def __init__(self, request):
        self.session = request.session
        user = request.user
        self.user = user
        cart = self.session.get('cart')
        if cart is None:
            cart = self.session['cart'] = {}
        self.cart = cart
            
    def add(self, dvd, quantity=1, update_quantity=False):
        dvd_id = str(dvd.id)
        if dvd_id not in self.cart:
            self.cart[dvd_id] = {'quantity': 0, 'price': str(dvd.price)}
        
        if update_quantity:
            self.cart[dvd_id]['quantity'] = quantity
        else:
            self.cart[dvd_id]['quantity'] += quantity
        
        self.save()
        
    def save(self):
        self.session.modified = True
    
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
            
    
    def __iter__(self):
        dvd_id  = self.cart.keys()
        dvds = movie.objects.filter(id__in=dvd_id)
        
        cart = self.cart.copy()
        for dvd in dvds:
            cart[str(dvd.id)]['dvd'] = dvd
            
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
            
    def create(self, order):
        cart = self.cart
        dvd_id = self.cart.keys()
        dvds = movie.objects.filter(id__in=dvd_id)
        order = Order.objects.get(id=order.id)
        
        
        for item in dvds:
            Dvd.objects.create(movie_dvd=item, owned=True, paid=True, user_dvd=self.user, movie_order=order)
    
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
        
    def get_total_price(self):
        return sum(Decimal(item['price'])*item['quantity'] for item in self.cart.values())
        
    def clear(self):
        del self.session['cart']
        self.save()