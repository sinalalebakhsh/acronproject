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
    p1.description = 'p1.description'
    p1.unit_price = 1000
    p1.inventory = 10

    product_2 = Product()
    product_2.name = 'product_2'
    product_2.category = new_category
    product_2.description = 'product_2.description'
    product_2.unit_price = 2200
    product_2.inventory = 220
    
    # ساخت Order بسیار ساده برای customer با id=1
    new_order = Order()
    new_order.customer_id = 1
    new_order.save()
    
    order_items_1 = OrderItem()
    order_items_1.product = p1

    order_items_2 = OrderItem()
    order_items_2.product = product_2
    order_items_2.product += product_2

    order_items_3 = OrderItem()
    order_items_3.product_id = 3
    order_items_3.product_id += 3
    order_items_3.product_id += 3

    return render(request, 'hello.html')



