from rest_framework.decorators import api_view
from rest_framework.response import Response


from store import models 
from store import serializers 

@api_view()
def product_list(request):
    return Response('Hello')



@api_view()
def product_detail(request, id):
    try:
        product = models.Product.objects.get(pk=id)
    except:
        return Response(status=404)
    serializer = serializers.Product_Serializer(product)

    return Response(serializer.data)



