from django.shortcuts import render
from django.http import HttpResponse

from .models import Product


def show_data(request):
    queryset = Product.objects.filter(inventory__lt=5)

    return render(request, 'hello.html', {'products': list(queryset)})



