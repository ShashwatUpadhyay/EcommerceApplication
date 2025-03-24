from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserExtra)

class AdressAdmin(admin.ModelAdmin):
    list_display = ['full_name','email','phone','country','state','city','address','pin_code','selected']
    list_filter = ['selected']
    search_fields = ['full_name','email','phone','country','state','city','address','pin_code','selected']
    list_editable = ['selected']

admin.site.register(Address,AdressAdmin)