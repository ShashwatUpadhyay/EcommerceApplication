from django.db import models
from django.contrib.auth.models import User
from account.models import UserExtra
from base.base_model import BaseModel
from shop.models import Product 

# Create your models here.
class Cart(BaseModel):
    customer  = models.ForeignKey(UserExtra, on_delete=models.CASCADE, related_name='cart')
    is_paid = models.BooleanField(default=False)
    
    def __str__(self):
        return self.customer.full_name 
    
class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    product = models.ForeignKey(Product, null=True,on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=0)
