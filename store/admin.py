from django.contrib import admin

from .models import Product
from .models import Category
from .models import Order


@admin.register(Product)
class Product_Admin(admin.ModelAdmin):
    list_display = ['id', 'name', 'inventory', 'inventory_status', 'unit_price', 'datetime_created']
    list_editable = ['name', 'inventory', 'unit_price']
    list_per_page = 20
    ordering = ['-datetime_created']

    def inventory_status(self, product_object):
        if product_object.inventory < 10:
            return 'less than 10'
        if product_object.inventory == 10:
            return 'equal with 10'
        else:
            return 'greater than 10'
# admin.site.register(Product, Product_Admin)


@admin.register(Order)
class Order_Admin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status', 'datetime_created']
    list_editable = ['status']
    list_per_page = 20
    ordering = ['-datetime_created']


@admin.register(Category):
class Cate
# admin.site.register(Category)






