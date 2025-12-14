from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F, Value, Func
from django.db.models import Count, Avg, Max
from django.core.paginator import Paginator


from .models import Product, OrderItem, Order, Comment, Customer


def show_data(request):    
    queryset = Customer.objects \
                        .annotate(orders_customer=Count('orders')) \
                        .all() \
    paginator = Paginator(customers, 50)  # 50 رکورد در هر صفحه
    page = paginator.get_page(1)
    print(queryset)
    return render(request, 'hello.html')



