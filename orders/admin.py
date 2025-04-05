from django.contrib import admin
from .models import *

# Register your models here.
class CartItemAdmin(admin.StackedInline):
    model = CartItem

class cartAdmin(admin.ModelAdmin):
    list_display = ['customer','order_taken','is_paid']
    list_filter = ['order_taken']
    inlines = [CartItemAdmin]

admin.site.register(Cart,cartAdmin)
admin.site.register(CartItem)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','status','is_paid','is_delivered']
    list_filter = ['is_paid','is_delivered','is_canceled','is_returned','is_refunded']
admin.site.register(Order,OrderAdmin)

class NonUserCartItemAdmin(admin.StackedInline):
    model = NonUserCartItem

class NonUserCartAdmin(admin.ModelAdmin):
    list_display = ['session_key','order_taken','is_paid']
    list_filter = ['order_taken']
    inlines = [NonUserCartItemAdmin]

admin.site.register(NonUserCart,NonUserCartAdmin)
admin.site.register(NonUserCartItem)
