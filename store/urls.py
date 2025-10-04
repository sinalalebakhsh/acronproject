from django.urls import path

from .views import say_hello

from . import views

urlpatterns = [
    path('hello/', say_hello),
    path('number/<int:numbers>', views.numbers_),
]

