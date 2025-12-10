from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F, Value
from django.db.models import Count, Avg, Max

from .models import Product, OrderItem, Order, Comment


def show_data(request):    
    queryset = OrderItem.objects.annotate(total_price=F('quantity') * F('unit_price')).all()
    
    print(list(queryset))
    return render(request, 'hello.html', { })



