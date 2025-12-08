from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F
from django.db.models import Count, Avg, Max

from .models import Product, OrderItem, Order, Comment


def show_data(request):    
    queryset = Product.objects.all()
    # To PUSH
    # list(queryset_orderitems_products)
    queryset_plus = Product.objects.filter(inventory__gt=10).aggregate(avregate_of_inventory_gt_10=Avg('unit_price'))
    
    return render(request, 'hello.html', {
        'order_items': list(queryset),
        'aggregate': queryset_plus,
        })



