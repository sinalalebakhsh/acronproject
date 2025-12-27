from django.contrib import admin

from .models import Product
from .models import Category



class Product_Admin(admin.ModelAdmin):
    list_display = ['id', 'name', 'inventory', 'unit_price']




admin.site.register(Product, Product_Admin)
admin.site.register(Category)






