from django.db import models
from base.base_model import BaseModel
from django.utils.text import slugify
from django.contrib.auth.models import User

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
    min_order_quanitity = models.PositiveIntegerField(default=1, verbose_name='Minimum order quantity')
    stock = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return str(self.title) 
    
    def latest_image(self):
        return self.image.last()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)



class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='image')
    img = models.ImageField(upload_to='product_images/')
    
    class Meta:
        get_latest_by = "created_at"
        
        
