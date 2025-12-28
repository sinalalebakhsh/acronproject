from django.contrib import admin

from .models import Product
from .models import Category
from .models import Order


@admin.register(Product)
class Product_Admin(admin.ModelAdmin):
    list_display = ['id', 'name', 'inventory', 'unit_price']
    list_editable = ['name', 'inventory', 'unit_price']
    list_per_page = 20
# admin.site.register(Product, Product_Admin)


@admin.register(Order)
class Order_Admin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status']



admin.site.register(Category)






