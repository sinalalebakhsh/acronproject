from django.urls import path

from rest_framework.decorators import api_view


from . import views



@api_view
urlpatterns = [
    path('products/', views.products_list),
]



