from django.apps import apps

def cart_context(request):
    Cart = apps.get_model('orders', 'Cart')
    
    def in_cart(product):
        return Cart.objects.filter(customer=request.user.extra,order_taken=False, cartitems__product=product).exists()
    
    return {'in_cart': in_cart}
