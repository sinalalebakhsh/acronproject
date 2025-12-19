from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F, Value, Func
from django.db.models import Count, Avg, Max
from django.db.models import ExpressionWrapper, DecimalField

from django.utils import timezone

from .models import (
    Category, 
    Product,
    Order,
    OrderItem,
    )


def show_data(request):    
    new_category = Category()
    new_category.title = 'A'
    new_category.description = 'aaa'

    p1 = Product()
    p1.name = 'p1'
    p1.category = new_category
    p1.slug = 'p-1'
    p1.description = 'p1.description'
    p1.unit_price = 1000
    p1.inventory = 1

    p2 = Product()
    p2.name = 'p2'
    p2.category = new_category
    p2.slug = 'p-2'
    p2.description = 'p2.description'
    p2.unit_price = 1000
    p2.inventory = 1
    # ساخت Order بسیار ساده برای customer با id=1
    new_order = Order()
    new_order.customer_id = 1
    new_order.save()
    
    order_items_1 = OrderItem()
    order_items_1.product = p1

    order_items_2 = OrderItem()
    order_items_2.product = p2
    order_items_2.product += p2

    order_items_3 = OrderItem()
    order_items_3.product_id = 3
    order_items_3.product_id += 3
    order_items_3.product_id += 3

    return render(request, 'hello.html')



