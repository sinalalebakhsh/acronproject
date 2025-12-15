from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F, Value, Func
from django.db.models import Count, Avg, Max
from django.db.models import ExpressionWrapper, DecimalField

from django.utils import timezone

from .models import Category, Product


def show_data(request):    
    # UPDATE

    # category = Category.objects.get(pk=97)
    # category.title= 'Cars'
    # category.description= 'cars are good.'
    # category.top_product__id= Product.objects.get(id=2)
    # category.save()

    category = Category.objects.filter(pk=96).update(title='AAAA')


    return render(request, 'hello.html')



