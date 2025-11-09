from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q

from .models import Product, OrderItem, Order


def show_data(request):
    queryset = Product.objects.filter(Q(inventory__lt=5) | Q(inventory__gt=96)).order_by('inventory')
    
    list(queryset)
    return render(request, 'hello.html',)



