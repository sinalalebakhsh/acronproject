



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

