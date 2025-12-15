from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F, Value, Func
from django.db.models import Count, Avg, Max
from django.db.models import ExpressionWrapper, DecimalField



from .models import Product, OrderItem, Order, Comment, Customer


def show_data(request):    
    queryset = OrderItem.SINA_.annotate(
        total_price=ExpressionWrapper(F('unit_price') * 0.5, output_field=DecimalField())
    )




    print(queryset)

    return render(request, 'hello.html', {"query": list(queryset)})



