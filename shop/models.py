from django.db import models
from base.base_model import BaseModel

# Create your models here.
class ProductCategory(BaseModel):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.name) 
    

class Product(BaseModel):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    price = models.IntegerField()
    
    def latest_image(self):
        return self.image.last()



class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='image')
    img = models.ImageField(upload_to='product_images/')
    
    class Meta:
        get_latest_by = "created_at"