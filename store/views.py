from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F

from .models import Product, OrderItem, Order


def show_data(request):    
    queryset = Product.objects.only('name', 'id')

    # list(queryset_orderitems_products)
    return render(request, 'hello.html', {'products': list(queryset)})



