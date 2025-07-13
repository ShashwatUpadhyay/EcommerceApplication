import random
from orders.models import Order 

def generate_unique_order_id():
    while True:
        order_id = random.randint(100000, 9999999)
        if not Order.objects.filter(order_number=order_id).exists():
            return order_id
        
    
def get_stock_status(stock):
    if stock == 0:
        return "Out of Stock"
    elif stock <= 5:
        return "Low Stock"
    else:
        return "In Stock"