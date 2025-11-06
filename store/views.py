from django.shortcuts import render
from django.http import HttpResponse

from .models import Product, OrderItem


def show_data(request):
    queryset = Product.objects.all()
    queryset = Product.objects.filter(inventory__lt=50)
    queryset = Product.objects.order_by('inventory')
    
    # queryset = OrderItem.objects.all()

    list(queryset)
    return render(request, 'hello.html',)



