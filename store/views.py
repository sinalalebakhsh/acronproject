from django.shortcuts import (
        get_object_or_404,
        render,
    )

from django.http import JsonResponse, HttpResponse




from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from store import models 
from store import serializers 
# from store.serializers import ProductSerializer 

@api_view()
def product_list(request):
    products_queryset = models.Product.objects.all()
    # return JsonResponse(products_queryset)
    # return JsonResponse(products_queryset)
    serializers__ = serializers.ProductSerializer(products_queryset, many=True)
    return Response(serializers__.data)



@api_view()
def product_detail(request, id):
    # try:
    #     product = models.Product.objects.get(pk=id)
    # except models.Product.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)
    # این خط دقیقا کار چهار خط بالا رو انجام میده
    product = get_object_or_404(models.Product, pk=id)

    serializer = serializers.ProductSerializer(product)

    return Response(serializer.data)



def json(request):
    json_data = {
        "a11":{"sina":"lale", "asd":123},
        "id":"1",
        "job":"PRO",
    }
        # "1": {
        #     "id":"1",
        #     "title":"first",
        #     "description":"XYZ..... ZYX",
        # },
        # "2": {
        #     "id":"2",
        #     "title":"second",
        #     "description":"XYZ..... ZYX",
        # },
        # "3": {
        #     "id":"3",
        #     "title":"third",
        #     "description":"XYZ..... ZYX",
        # },
        # "4": {
        #     "id":"4",
        #     "title":"fourd",
        #     "description":"XYZ..... ZYX",
        # },


    my_dictionary = json_data
    return render(request, "store/home.html", context=my_dictionary)
    # return JsonResponse({
    #     "KEY-1":"VALUE-1",
    #     "KEY-2":"VALUE-2",
    #     "KEY-3":"VALUE-3",
    #     "KEY-4":"VALUE-4",
    # })


