from django.contrib import admin
from .models import *

# Register your models here.
class CartItemAdmin(admin.StackedInline):
    model = CartItem

class cartAdmin(admin.ModelAdmin):
    list_display = ['customer','is_paid']
    list_filter = ['is_paid']
    inlines = [CartItemAdmin]

admin.site.register(Cart,cartAdmin)
admin.site.register(CartItem)
