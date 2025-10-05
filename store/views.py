from django.shortcuts import render
from django.http import HttpResponse

def say_hello(request, namess):
    return render(request, 'hello.html' , context={"namess": namess})


def numbers_(request, numbers):
    return HttpResponse(numbers)


