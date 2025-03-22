from django.db import models
from django.contrib.auth.models import User
from account.models import UserExtra
from base.base_model import BaseModel
from shop.models import Product 
from account.models import Address

# Create your models here.
class Cart(BaseModel):
    customer  = models.ForeignKey(UserExtra, on_delete=models.CASCADE, related_name='cart')
    is_paid = models.BooleanField(default=False)
    
    @property
    def items(self):
        return self.cartitems.all().count()
    
    @property
    def total_price(self):
        items = sum(item.product.price * item.quantity for item in self.cartitems.all())
        return items
    
    @property
    def tax(self):
        return (self.total_price/100)* 18
    
    @property
    def final_price(self):
        return self.total_price + self.tax
    
    def __str__(self):
        return self.customer.full_name 
    
class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    product = models.ForeignKey(Product, null=True,on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=0)
    
class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    address = models.ForeignKey(Address , on_delete=models.DO_NOTHING)