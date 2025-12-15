from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F, Value, Func
from django.db.models import Count, Avg, Max
from django.db.models import ExpressionWrapper, DecimalField



from .models import Product, OrderItem, Order, Comment, Customer


def show_data(request):    
    # product_1 = Product.objects.get(id=1)

    Comment.objects.create(
        product_id=1,
        name='SINA LALEHBAKHSH',
        body='Sina is DjangoDeveloper and DevOps Engineer',
    )

    return render(request, 'hello.html')



