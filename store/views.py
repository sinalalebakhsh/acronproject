from django.shortcuts import render
from django.http import HttpResponse

from .models import Product, OrderItem, Order


def show_data(request):
    queryset = Order.objects.filter(status=Order.ORDER_STATUS_UNPAID)
    
    list(queryset)
    return render(request, 'hello.html',)



