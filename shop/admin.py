from django.contrib import admin
from .models import *
# Register your models here.

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
class ProductFeatureAdmin(admin.StackedInline):
    model = ProductFeature
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price','category']
    list_filter = ['category__name']
    inlines = [ProductFeatureAdmin,ProductImageAdmin]
    list_per_page = 20
    search_fields = ['title','category__name']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Product,ProductAdmin)
admin.site.register(ProductCategory)
admin.site.register(ProductImage)
admin.site.register(ProductSubCategory)
admin.site.register(Whislist)
