from django.shortcuts import get_object_or_404,render
from django.db.models import Prefetch
# from django.http import JsonResponse, HttpResponse

from rest_framework.decorators import api_view
# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
# from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, DjangoModelPermissions

from django_filters.rest_framework import DjangoFilterBackend


from .paginations import DefaultPagination
from store import models 
from store import serializers 
from .filters import ProductFilter
from .permissions import CustomDjangoModelPermissions, IsAdminOrReadOnly, SendPrivateEmailToCustomerPermission


""" PRODUCT """
class ProductViewSet(ModelViewSet):
    serializer_class = serializers.ProductSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['name', 'unit_price', 'inventory',]
    search_fields = ['name', ]

    permission_classes = [IsAdminOrReadOnly]

    pagination_class = DefaultPagination
    # pagination_class = PageNumberPagination
    
    # filterset_fields = ['category_id', 'unit_price' , 'inventory' ]
    filterset_class = ProductFilter

    queryset = models.Product.objects.all()    
    def get_parser_context(self, http_request):
        return {"request": self.request}
    # def get_queryset(self):
    #     queryset = models.Product.objects.all()
    #     category_id_parameter = self.request.query_params.get('category_id') 
    #     if category_id_parameter is not None:
    #         queryset = queryset.filter(category_id=category_id_parameter)
    #     return queryset
    # queryset = models.Product.objects.select_related("category").all()


class ProductsPOST(CreateAPIView):
    serializer_class = serializers.ProductSerializer



""" CATEGORY """
class CategoryViewSet(ModelViewSet):
    queryset = models.Category.objects.prefetch_related("products")
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


    def delete(self, request, pk):
        category = get_object_or_404(models.Category.objects.prefetch_related("products"), pk=pk)
        if category.products.count() > 0:
            return Response({'Error': "1)First: remove the order items. 2) Remove this."})
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


""" COMMENT """
class CommentViewSet(ModelViewSet):
    # queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    # queryset = models.Comment.objects.all()


    def get_queryset(self):
        product_pk = self.kwargs['product_pk']
        return models.Comment.objects.filter(product_id=product_pk).all()


    def get_serializer_context(self):
        return {'product_pk': self.kwargs['product_pk']}


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'path', 'delete', ]
    # serializer_class = serializers.CartItemSerializer
    
    def get_queryset(self):
        cart_pk = self.kwargs['cart_pk']
        return models.CartItem.objects.select_related('product').filter(cart_id=cart_pk).all()


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.AddCartItemSerializer
        elif self.request.method == 'PATH':
            return serializers.UpdateCartItemSerializer
        return serializers.CartItemSerializer

    def get_serializer_context(self):
        return {'cart_pk': self.kwargs['cart_pk']}



class CartViewSet(CreateModelMixin,
                   RetrieveModelMixin,
                   DestroyModelMixin,
                   GenericViewSet):
    serializer_class = serializers.CartSerializer
    queryset = models.Cart.objects.prefetch_related('items__product').all()
    lookup_value_regex = r'[0-9a-fA-F]{8}\-?[0-9a-fA-F]{4}\-?[0-9a-fA-F]{4}\-?[0-9a-fA-F]{4}\-?[0-9a-fA-F]{12}'


class CustomerViewSet(ModelViewSet):
    serializer_class = serializers.CustomerSerializer
    queryset = models.Customer.objects.all()
    permission_classes = [IsAdminUser]


    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user_id = request.user.id
        customer = models.Customer.objects.get(user_id=user_id)
        if request.method == 'GET':
            serializer = serializers.CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = serializers.CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(detail=True, permission_classes=[SendPrivateEmailToCustomerPermission])
    def send_private_email(self, request, pk):
        customer = self.get_object()
        # send email to customer by the button
        return Response({'message': 'Email sent successfully.', 'Private Key User ID': f'{pk}'})


class OrderViewSet(ModelViewSet):
    serializer_class = serializers.OrderSerializer


    #                      .prefetch_related('items__product').
    # queryset = models.Order.objects.prefetch_related('items').all()

    def get_queryset(self):
        # return models.Order.objects.prefetch_related('items__product').all()
        return models.Order.objects.prefetch_related(
            Prefetch(
                'items',
                queryset = models.OrderItem.objects.select_related('product'),
            )
        ).all()




""" ## class ProductList(ListCreateAPIView): + class ProductDetail(RetrieveUpdateDestroyAPIView):
# class ProductList(ListCreateAPIView):
#     serializer_class = serializers.ProductSerializer
#     queryset = models.Product.objects.select_related("category").all()
#     def get_parser_context(self, http_request):
#         return {"request": self.request}
#     def delete(self, request, pk):
#         product = get_object_or_404(
#             models.Product.objects.select_related("category"), 
#             pk=pk
#         )
#         if product.order_items.count() > 0:
#             return Response({'Error': "1)First: remove the order items. 2) Remove this."})
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = serializers.ProductSerializer
#     queryset = models.Product.objects.select_related("category").all()
#     def delete(self, request, pk):
#         product = get_object_or_404(
#             models.Product.objects.select_related("category"), 
#             pk=pk
#         )
#         if product.order_items.count() > 0:
#             return Response({'Error': "1)First: remove the order items. 2) Remove this."})
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
"""

""" ## class CategoryList(ListCreateAPIView): + class CategorieDetail(RetrieveUpdateDestroyAPIView):
# class CategoryList(ListCreateAPIView):
#     queryset = models.Category.objects.prefetch_related("products")
#     serializer_class = serializers.CategorySerializer

# class CategorieDetail(RetrieveUpdateDestroyAPIView):
#     queryset = models.Category.objects.prefetch_related("products").all()
#     serializer_class = serializers.CategorySerializer
#     def delete(self, request, pk):
#         category = get_object_or_404(models.Category.objects.prefetch_related("products"), pk=pk)
#         if category.products.count() > 0:
#             return Response({'Error': "1)First: remove the order items. 2) Remove this."})
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
"""

""" class CategorieDetail(APIView):
# class CategorieDetail(APIView):
#     def get(self, request, pk):
#         category = get_object_or_404(models.Category.objects.prefetch_related("products"), pk=pk)
#         serializer = serializers.CategorySerializer(category)
#         return Response(serializer.data)
#     def put(self, request, pk):
#         category = get_object_or_404(models.Category.objects.prefetch_related("products"), pk=pk)
#         serializer = serializers.CategorySerializer(category , data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     def delete(self, request, pk):
#         category = get_object_or_404(models.Category.objects.prefetch_related("products"), pk=pk)
#         if category.products.count() > 0:
#             return Response({'Error': "1)First: remove the order items. 2) Remove this."})
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
"""

# تمام کلاس پایین در دو خط در کلاس بالا 
# جمع شد و قابل استفاده با همان امکانات هست
""" class CategoryList(APIView):
class CategoryList(APIView):
    def get(self, request):
        categories_queryset = models.Category.objects.prefetch_related("products")
        serializer = serializers.CategorySerializer(
            categories_queryset,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
"""

""" class ProductsPOST(APIView):
# class ProductsPOST(APIView):
#     def post(self, request):
#         serializer = serializers.ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

"""

""" class ProductDetail(APIView):
# class ProductDetail(APIView):
#     def get(self, request, pk):
#         product = get_object_or_404(
#             models.Product.objects.select_related("category"), 
#             pk=pk
#         )
#         serializer = serializers.ProductSerializer(
#             product,
#             context={"request": request},
#         )
#         return Response(serializer.data)

#     def put(self, request, pk):
#         product = get_object_or_404(
#             models.Product.objects.select_related("category"), 
#             pk=pk
#         )
#         serializer = serializers.ProductSerializer(product , data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def delete(self, request, pk):
#         product = get_object_or_404(
#             models.Product.objects.select_related("category"), 
#             pk=pk
#         )
#         if product.order_items.count() > 0:
#             return Response({'Error': "1)First: remove the order items. 2) Remove this."})
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

"""

""" class ProductList(ListCreateAPIView):
# برای اینکه تعداد خطوط کد ها کمتر بشه قابلیت ها، به کلاس اضافه شد 
# ولی از کلاس بالا خطوط کامنت رو پاک کردم
# تمام اون خطوط پاک شده زیر این خط موجود هست
class ProductList(ListCreateAPIView):
    serializer_class = serializers.ProductSerializer
    # خط پایین رو در صورتی با خط بالا جایگزین میکنیم که بخوایم کد اضافه کنیم 
    # def get_serializer_class(self):
    #     return serializers.ProductSerializer
    
    queryset = models.Product.objects.select_related("category").all()
    # خط پایین رو در صورتی با خط بالا جایگزین میکنیم که بخوایم کد اضافه کنیم 
    # def get_queryset(self):
    #     return models.Product.objects.select_related("category").all()

    def get_parser_context(self, http_request):
        return {"request": self.request}


# class ProductList(APIView)
class ProductList(APIView):
    def get(self, request):
        products_queryset = models.Product.objects.select_related("category").all()
        serializer = serializers.ProductSerializer(
                products_queryset, 
                many=True,
                context={"request": request},
            )
        return Response(serializer.data)
    def post(self, request):
        serializer = serializers.ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
"""

""" def category_detail(request, pk):
# @api_view(['GET', 'PUT', 'DELETE'])
# def category_detail(request, pk):
#     category = get_object_or_404(models.Category.objects.annotate(
#             products_count=Count("products")
#         ).all(), pk=pk)
#     if request.method == 'GET':
#         serializer = serializers.CategorySerializer(category)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = serializers.CategorySerializer(category , data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if category.products.count() > 0:
#             return Response({'Error': "1)First: remove the order items. 2) Remove this."})
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
"""

"""def categories(request):
# @api_view(['GET', 'POST'])
# def categories(request):
#     if request.method == 'GET':
#         categories_queryset = models.Category.objects.annotate(
#             products_count=Count("products")
#         ).all()
#         serializer = serializers.CategorySerializer(
#             categories_queryset,
#             many=True,
#         )
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = serializers.CategorySerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
"""

"""def json(request):
# def json(request):
#     json_data = {
#         "a11":{"sina":"lale", "asd":123},
#         "id":"1",
#         "job":"PRO",
#     }
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


    # my_dictionary = json_data
    # return render(request, "store/home.html", context=my_dictionary)
    # return JsonResponse({
    #     "KEY-1":"VALUE-1",
    #     "KEY-2":"VALUE-2",
    #     "KEY-3":"VALUE-3",
    #     "KEY-4":"VALUE-4",
    # })
"""

"""def product_list(request):
# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == 'GET':
#         products_queryset = models.Product.objects.select_related("category").all()
#         # return JsonResponse(products_queryset)
#         # return JsonResponse(products_queryset)
#         serializer = serializers.ProductSerializer(
#                 products_queryset, 
#                 many=True,
#                 context={"request": request},
#             )
#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         serializer = serializers.ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#         # if serializer.is_valid():
#         #     serializer.validated_data
#         #     return Response("Everything is OK |||| serializer.validated_data")
#         # else:
#         #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         # return Response("All OK!")
"""

"""def product_detail(request, pk):
# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail(request, pk):
#     product = get_object_or_404(
#         models.Product.objects.select_related("category"), 
#         pk=pk
#     )
#     if request.method == 'GET':
#         serializer = serializers.ProductSerializer(
#             product,
#             context={"request": request},
#         )
#         return Response(serializer.data)
#         # try:
#         #     product = models.Product.objects.get(pk=pk)
#         # except models.Product.DoesNotExist:
#         #     return Response(status=status.HTTP_404_NOT_FOUND)
#         # این خط دقیقا کار چهار خط بالا رو انجام میده

#     elif request.method == 'PUT':
#         serializer = serializers.ProductSerializer(product , data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
#     elif request.method == 'DELETE':
#         if product.order_items.count() > 0:
#             return Response({'Error': "1)First: remove the order items. 2) Remove this."})
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
"""

"""def products_just_POST(request):
# @api_view(['POST'])
# def products_just_POST(request):
#     serializer = serializers.ProductSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data, status=status.HTTP_201_CREATED)
"""
