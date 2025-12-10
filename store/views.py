from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F, Value
from django.db.models import Count, Avg, Max

from .models import Product, OrderItem, Order, Comment


def show_data(request):    
    queryset = Product.objects.annotate(x=Value(1)).all()[:5]
    
       
    return render(request, 'hello.html', {
        

        })



