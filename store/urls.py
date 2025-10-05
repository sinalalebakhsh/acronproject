from django.urls import path

from .views import say_hello

from . import views

urlpatterns = [
    path('hello/<namess>', say_hello),
    path('number/<int:numbers>', views.numbers_),
]

