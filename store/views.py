from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F

from .models import Product, OrderItem, Order


def show_data(request):
    queryset_orderitems_products = OrderItem.objects.values('product_id').distinct() # delete repetetive products if had to 
    
    queryset = Product.objects.filter(id__in=queryset_orderitems_products)

    # list(queryset_orderitems_products)
    return render(request, 'hello.html', {'products': list(queryset)})



