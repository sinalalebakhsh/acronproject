from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F, Value, Func
from django.db.models import Count, Avg, Max
from django.db.models import ExpressionWrapper, DecimalField

from django.utils import timezone

from .models import Category, Product


def show_data(request):    

    # UPDATE
    category = Category(id=100)
    category.title= 'Cars'
    category.description= 'cars are good.'
    category.top_product= Product.objects.get(id=1)
    category.detetime_created= timezone.now()
    category.save()

    return render(request, 'hello.html')



