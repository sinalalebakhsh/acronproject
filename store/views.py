from django.shortcuts import (
        get_object_or_404,
        render,
    )

from django.http import JsonResponse, HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response


from store import models 
from store import serializers 
# from store.serializers import ProductSerializer 

@api_view()
def product_list(request):
    products_queryset = models.Product.objects.select_related("category").all()
    # return JsonResponse(products_queryset)
    # return JsonResponse(products_queryset)
    serializer = serializers.ProductSerializer(
            products_queryset, 
            many=True,
            context={"request": request},
        )
    return Response(serializer.data)



@api_view(['GET', 'POST'])
def product_detail(request, pk):
    if request.method == 'GET':
        product = get_object_or_404(
            models.Product.objects.select_related("category"), 
            pk=pk
        )
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
    elif request.method == 'POST':
        serializer = serializers.ProductSerializer(data=request.data)
        if serializer.is_valid():
            pass
        else:
            return Response(serializer.errors, status=status)
        return Response("All OK!")


@api_view()
def category_detail(request, pk):
    category = get_object_or_404(models.Category, pk=pk)
    serializer = serializers.CategorySerializer(category)
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


