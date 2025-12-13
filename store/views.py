from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F, Value, Func
from django.db.models import Count, Avg, Max

from .models import Product, OrderItem, Order, Comment, Customer


def show_data(request):    
    queryset = Order.objects \
                        .annotate(items_count=Count('items'))
    print(queryset)
    return render(request, 'hello.html')



