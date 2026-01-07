from django.shortcuts import get_object_or_404


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from store import models 
from store import serializers 

@api_view()
def product_list(request):
    products_queryset = models.Product.objects.all()
    serializers = serializers.ProductSerializer(products_queryset)
    return Response(serializers.data)



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



