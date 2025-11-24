from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F

from .models import Product, OrderItem, Order, Comment


def show_data(request):    
    queryset = Comment.objects.prefetch_related('product').all()
    # To PUSH
    # list(queryset_orderitems_products)
    return render(request, 'hello.html', {'comments': list(queryset)})



