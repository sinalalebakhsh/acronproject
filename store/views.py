from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F, Value, Func
from django.db.models import Count, Avg, Max
from django.db.models import ExpressionWrapper, DecimalField

from django.utils import timezone

from .models import Category, Product


def show_data(request):    

    # DELETE


    Category.objects.filter(pk=80).delete()


    # cat = Category(pk=94)
    # cat.delete()

    return render(request, 'hello.html')



