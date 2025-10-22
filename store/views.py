from django.shortcuts import render
from django.http import HttpResponse

def say_hello(request, namess):
    a = 2
    b = a * 2
    return render(request, 'hello.html' , context={'namess': namess, 'b': b})


def numbers_(request, numbers):
    return HttpResponse(numbers)


