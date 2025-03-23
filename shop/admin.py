from django.contrib import admin
from .models import *
# Register your models here.

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price','category']
    list_filter = ['category__name']
    inlines = [ProductImageAdmin]

admin.site.register(Product,ProductAdmin)
admin.site.register(ProductCategory)
admin.site.register(ProductImage)
admin.site.register(ProductSubCategory)
