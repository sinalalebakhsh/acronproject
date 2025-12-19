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
    # CREATE
    """
        cat = Category.objects.create(title='Z', description='ZZZZ',top_product_id=1)
        new_category = Category()
        new_category.title = 'A'
        new_category.description = 'aaa'
        new_category.top_product_id = 1
        new_category.save()
        p1 = Product()
        p1.name = 'p1'
        p1.category = new_category
        p1.slug = 'p-1'
        p1.description = 'p1.description'
        p1.unit_price = 1000
        p1.inventory = 1
        p1.save()
        p2 = Product()
        p2.name = 'p2'
        p2.category = new_category
        p2.slug = 'p-2'
        p2.description = 'p2.description'
        p2.unit_price = 2000
        p2.inventory = 2
        p2.save()
        # ساخت Order بسیار ساده برای customer با id=1
        new_order = Order()
        new_order.customer_id = 1
        new_order.save()
        order = Order.objects.create(customer_id=1)
        order_item_1 = OrderItem.objects.create(
            order=order,
            product=p1,
            quantity=10,
            unit_price=p1.unit_price,
        )
        order_item_2 = OrderItem.objects.create(
            order=order,
            product=p2,
            quantity=20,
            unit_price=p2.unit_price,
        )
        order_item_3 = OrderItem.objects.create(
            order=order,
            product_id=1,
            quantity=30,
            unit_price=1000,
        )
        order_items_1 = OrderItem()
        order_items_1.order = order
        order_items_1.product = p1
        order_items_1.quantity = 10
        order_items_1.unit_price = p1.unit_price
        order_items_2 = OrderItem()
        order_items_2.product = p2
        order_items_2.product += p2
        order_items_3 = OrderItem()
        order_items_3.product_id = 3
        order_items_3.product_id += 3
        order_items_3.product_id += 3
    """

    # UPDATE
    Product.objects.filter(name=)
    return render(request, 'hello.html')



