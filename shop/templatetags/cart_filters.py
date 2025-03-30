from django import template
from django.apps import apps


register = template.Library()

@register.filter(name='in_cart')
def in_cart(product, user):
    Cart = apps.get_model('orders', 'Cart')  # Lazy import to prevent circular import
    return Cart.objects.filter(customer=user.extra,order_taken=False, cartitems__product=product).exists()

@register.filter(name='in_wishlist')
def in_wishlist(product, user):
    wishlist = apps.get_model('shop', 'Whislist')
    return wishlist.objects.filter(user=user, product=product).exists()
