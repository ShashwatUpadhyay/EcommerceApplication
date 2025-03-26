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
    order_taken = models.BooleanField(default=False)
    
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
    
    @property
    def all_items(self):
        return self.cartitems.all()
    
    def __str__(self):
        return self.customer.full_name 
    
class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    product = models.ForeignKey(Product, null=True,on_delete=models.SET_NULL, related_name='incart')
    quantity = models.IntegerField(default=0)
    
    @property
    def total_price(self):
        return self.product.price * self.quantity
    
    @property
    def total_tax(self):
        return (self.total_price/100)* 18
    
    @property
    def final_price(self):
        return self.total_price + self.total_tax
    
class Order(BaseModel):
    status_choices = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled'),
        ('Returned', 'Returned'),
        ('Refunded', 'Refunded'),
    )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='orders')
    address = models.ForeignKey(Address , on_delete=models.DO_NOTHING, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='order')
    status = models.CharField(max_length=100, choices=status_choices, default='Pending')
    is_paid = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=200, null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=200, null=True, blank=True) 
    razorpay_payment_id = models.CharField(max_length=200, null=True, blank=True)   
    razorpay_signature = models.CharField(max_length=200, null=True, blank=True)    
    is_delivered = models.BooleanField(default=False)
    delevery_date = models.DateTimeField(null=True, blank=True)
    is_canceled = models.BooleanField(default=False)
    canceled_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    returned_date = models.DateTimeField(null=True, blank=True)
    is_refunded = models.BooleanField(default=False)
    refunded_date = models.DateTimeField(null=True, blank=True)
   
    def __str__(self):
        return self.user.extra.full_name
    
    class Meta:
        ordering = ['-created_at']  
        
@receiver(post_save, sender=CartItem)
def resultAnounced(sender, instance, created, **kwargs):
    if created:
        instance.quantity = instance.product.min_order_quanitity-1
        instance.save()