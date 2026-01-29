# pipenv change host
```
set PIP_TRUSTED_HOST=mirror-pypi.runflare.com
```
than
```
pipenv install drf-nested-routers
```

# Select Related:
```

@admin.register(Product)
class Product_Admin(admin.ModelAdmin):
    list_display = ['id', 'name', 'inventory', 'inventory_status', 'unit_price', 'datetime_created', 'product_category']
    list_editable = ['name', 'inventory', 'unit_price']
    list_per_page = 20
    ordering = ['-datetime_created']
    list_select_related = ['category']

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
```


# Prefetch Related 
```
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
```

## dipendent ...

```
pipenv install drf-nested-routers
```

