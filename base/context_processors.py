from orders.models import Cart

def cart_item_count(request):
    if request.user.is_authenticated:
        try:
            customer = request.user.extra
            cart =  Cart.objects.get(customer=customer) 
            count = cart.cartitems.count() 
        except Cart.DoesNotExist:
            count = 0
    else:
        count = 0  # For anonymous users, cart is empty

    return {'cart_item_count': count}
