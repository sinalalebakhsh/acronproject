from django.shortcuts import render
from django.http import HttpResponse

from .models import Product


def show_data(request):
    qq = Product.objects.all()

    print(qq[1])

    return render(request, 'hello.html')



