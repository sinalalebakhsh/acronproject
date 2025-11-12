from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F

from .models import Product, OrderItem, Order


def show_data(request):
    queryset = Product.objects.values('id', 'name', 'unit_price')
    
    list(queryset)
    return render(request, 'hello.html',)



