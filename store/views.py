from django.shortcuts import (
        get_object_or_404,
        render,
    )

from django.db.models import Count

from django.http import JsonResponse, HttpResponse

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from store import models 
from store import serializers 
# from store.serializers import ProductSerializer 


class ProductList(APIView):
    def get():
        



@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        products_queryset = models.Product.objects.select_related("category").all()
        # return JsonResponse(products_queryset)
        # return JsonResponse(products_queryset)
        serializer = serializers.ProductSerializer(
                products_queryset, 
                many=True,
                context={"request": request},
            )
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = serializers.ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        # if serializer.is_valid():
        #     serializer.validated_data
        #     return Response("Everything is OK |||| serializer.validated_data")
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response("All OK!")

@api_view(['POST'])
def products_just_POST(request):
    serializer = serializers.ProductSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)




@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    product = get_object_or_404(
        models.Product.objects.select_related("category"), 
        pk=pk
    )
    if request.method == 'GET':
        serializer = serializers.ProductSerializer(
            product,
            context={"request": request},
        )
        return Response(serializer.data)
        # try:
        #     product = models.Product.objects.get(pk=pk)
        # except models.Product.DoesNotExist:
        #     return Response(status=status.HTTP_404_NOT_FOUND)
        # این خط دقیقا کار چهار خط بالا رو انجام میده

    elif request.method == 'PUT':
        serializer = serializers.ProductSerializer(product , data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        if product.order_items.count() > 0:
            return Response({'Error': "1)First: remove the order items. 2) Remove this."})
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
def categories(request):
    if request.method == 'GET':
        categories_queryset = models.Category.objects.annotate(
            products_count=Count("products")
        ).all()
        serializer = serializers.CategorySerializer(
            categories_queryset,
            many=True,
        )
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = serializers.CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    category = get_object_or_404(models.Category.objects.annotate(
            products_count=Count("products")
        ).all(), pk=pk)
    if request.method == 'GET':
        serializer = serializers.CategorySerializer(category)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = serializers.CategorySerializer(category , data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if category.products.count() > 0:
            return Response({'Error': "1)First: remove the order items. 2) Remove this."})
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)











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


