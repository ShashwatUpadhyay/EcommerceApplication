from orders.models import Cart, NonUserCart

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
        count = 0

    return {'cart_item_count': count}


def non_user_cart_item_count(request):
    key = request.session.get('eci',None)
    count = 0
    if key is not None: 
        try:
            cart = NonUserCart.objects.get(session_key=key)
            count = cart.items.count()
        except Exception as e:
            count = 0
    else:
        count = 0
    return {'non_user_cart_item_count': count}
