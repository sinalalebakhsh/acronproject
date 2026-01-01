from django.contrib import admin
from django.db.models import Count


from .models import (
    Product,
    Category,
    Order,
    Order,
    Comment,
)



class Inventory_Filter(admin.SimpleListFilter):
    title = 'Critical Inventory Status'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'High'),
            ('==10', 'Medium'),
            ('>10', 'OK'),
        ]
    
    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        if self.value() == '==10':
            return queryset.filter(inventory__lt=11, inventory__gt=9)
        if self.value() == '>10':
            return queryset.filter(inventory__gt=10)




@admin.register(Product)
class Product_Admin(admin.ModelAdmin):
    list_display = ['id', 'name', 'inventory', 'inventory_status', 'unit_price', 'datetime_created', 'product_category']
    list_editable = ['name', 'inventory', 'unit_price']
    list_per_page = 20
    ordering = ['-datetime_created']
    list_select_related = ['category']
    list_filter = ['datetime_created', 'category', Inventory_Filter]
#   list_filter = ['datetime_created', 'category']


    @admin.display(ordering='category__title')
    def product_category(self, product):
        return product.category.title

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
    list_display = ['id', 'customer', 'status', 'datetime_created', 'all_items_number']
    list_editable = ['status']
    list_per_page = 20
    ordering = ['-datetime_created']

    def get_queryset(self, request):
        return super()\
            .get_queryset(request)\
            .prefetch_related('items')\
            .annotate(
                items__count=Count('items')
            )
    
    @admin.display(ordering='items__count')
    def all_items_number(self, order):
        return order.items__count
        # خط بالا و پاینن ، تفاوتی با هم ندارند
        # return order.items.count()


    

@admin.register(Category)
class Category_Admin(admin.ModelAdmin):
    list_display = ['id', 'title', 'detetime_created', 'top_product']
    list_editable = ['title', 'top_product']
    list_per_page = 20
    ordering = ['-detetime_created']
# admin.site.register(Category)


@admin.register(Comment)
class Comment_Admin(admin.ModelAdmin):
    list_display = ['id','product','name','status','datetime_created']
    list_editable = ['product']
    list_per_page = 20
    ordering = ['-datetime_created']



