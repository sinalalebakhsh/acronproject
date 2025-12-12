from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F, Value, Func
from django.db.models import Count, Avg, Max

from .models import Product, OrderItem, Order, Comment, Customer


def show_data(request):    
    queryset = OrderItem.objects \
                        .values('order_id') \
                        .annotate(count=Count('order_id'))
    print(queryset)
    return render(request, 'hello.html')



