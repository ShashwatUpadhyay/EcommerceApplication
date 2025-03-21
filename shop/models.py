from django.db import models
from base.base_model import BaseModel
from django.utils.text import slugify

# Create your models here.
class ProductCategory(BaseModel):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.name) 
    

class Product(BaseModel):
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)
    
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