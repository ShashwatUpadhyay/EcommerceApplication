from orders.models import Cart

def cart_item_count(request):
    if request.user.is_authenticated:
        try:
            customer = None
            cart = None
            count = 0
            if not request.user.is_superuser:
                customer = request.user.extra
            if customer:
                cart =  Cart.objects.get(customer=customer,order_taken=False) 
                count = cart.cartitems.count() 
        except Cart.DoesNotExist:
            count = 0
    else:
        count = 0  # For anonymous users, cart is empty

    return {'cart_item_count': count}
