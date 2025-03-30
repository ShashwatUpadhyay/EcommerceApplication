from django.db import models
from base.base_model import BaseModel
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.apps import apps
# Create your models here.
class ProductCategory(BaseModel):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50, null=True, blank=True)
    img = models.ImageField(upload_to='category_images/', null=True, blank=True)
    
    def __str__(self):
        return str(self.name) 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(ProductCategory, self).save(*args, **kwargs)
    
class ProductSubCategory(BaseModel):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50, null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='sub_category')

    def __str__(self):
        return f'{str(self.name)}'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(ProductSubCategory, self).save(*args, **kwargs)

class Product(BaseModel):
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL,null=True, related_name='products')
    subcategory = models.ForeignKey(ProductSubCategory, on_delete=models.SET_NULL,null=True,blank=True)
    description = models.TextField()
    price = models.FloatField()
    old_price = models.FloatField(null=True, blank=True)
    min_order_quanitity = models.PositiveIntegerField(default=1, verbose_name='Minimum order quantity')
    stock = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return str(self.title) 
    
    def latest_image(self):
        return self.image.last()

    @property
    def in_cart(self, user):
        Cart = apps.get_model('orders', 'Cart')  
        return user.extra in Cart.objects.filter(customer=user.extra, is_paid=False, cartitems__product=self)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)



class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='image')
    img = models.ImageField(upload_to='product_images/')
    
    class Meta:
        get_latest_by = "created_at"
        
class ProductFeature(BaseModel):
    ICON_CHOICES = (
        ('fa fa-check text-green-500', 'Check Mark'),
        ('fa fa-times text-red-500', 'Cross/X Mark'),
        ('fa fa-star text-yellow-500', 'Star'),
        ('fa fa-heart text-red-700', 'Heart'),
        ('fa fa-bolt text-yellow-400', 'Bolt'),
        ('fa fa-leaf text-green-600', 'Leaf'),
        ('fa fa-shield text-blue-500', 'Shield'),
        ('fa fa-truck text-indigo-500', 'Truck'),
        ('fa fa-lock text-gray-600', 'Lock'),
        ('fa fa-battery-full text-green-600', 'Battery'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='features')
    icon = models.CharField(max_length=60, choices=ICON_CHOICES, default='fa fa-check text-green-500')
    feature = models.TextField()
    
    def __str__(self):
        return str(self.feature)
        

class Whislist(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='whishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='whishlist_product')
    

    class Meta:
        unique_together = ('user', 'product')  
    
    def __str__(self):
        return str(self.product.title)
