from django.shortcuts import render
from django.http import HttpResponse

from .models import Product


def show_data(request):
    query_ = Product.objects.get(id=1)

    print("-------------------------------------------------------------------------")
    print(query_.id)
    print(query_.name)
    print("-------------------------------------------------------------------------")

    return render(request, 'hello.html')



