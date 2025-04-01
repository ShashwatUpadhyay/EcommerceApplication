from django.db import models
from django.contrib.auth.models import User
from account.models import UserExtra
from base.base_model import BaseModel
from shop.models import Product 
from account.models import Address
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

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
        return items if items else 0
    
    @property
    def tax(self):
        return (self.total_price/100)* 18
    
    @property
    def final_price(self):
        return self.total_price + self.tax
    
    @property
    def all_items(self):
        return self.cartitems.all()
    
    def __str__(self):
        return self.customer.full_name 
    
class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    product = models.ForeignKey(Product, null=True,on_delete=models.SET_NULL, related_name='incart')
    quantity = models.IntegerField(default=0)
    
class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    address = models.ForeignKey(Address , on_delete=models.DO_NOTHING)
    
    
@receiver(post_save, sender=CartItem)
def resultAnounced(sender, instance, created, **kwargs):
    if created:
        instance.quantity = instance.product.min_order_quanitity-1
        instance.save()