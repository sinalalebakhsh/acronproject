from django.shortcuts import render
from django.http import HttpResponse

def say_hello(request):
    return render(request, 'hello.html' )


def numbers_(request, numbers):
    return HttpResponse(numbers)


