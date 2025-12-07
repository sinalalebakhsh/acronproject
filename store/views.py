from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F

from .models import Product, OrderItem, Order, Comment


def show_data(request):    
    queryset = Product.objects.all()
    # To PUSH
    # list(queryset_orderitems_products)
    print(queryset[0])
    return render(request, 'hello.html')



