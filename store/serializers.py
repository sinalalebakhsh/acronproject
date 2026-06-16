from django.utils.text import slugify
from decimal import Decimal
from rest_framework import serializers

from store import models
from store.models import Cart, CartItem, Category, Customer, Product, Comment


""" PRODUCT """
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'with_task', 'category', 'inventory',  'description']

    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')

    with_task = serializers.SerializerMethodField()
    def get_with_task(self, product):
        return round(product.unit_price * Decimal(1.09), 2)

    def validate(self, data):
        print(data)
        if len(data['name']) < 6:
            raise serializers.ValidationError("Product title length < 6 !!!")
        return data

    def create(self, validated_data):
        product = Product(**validated_data)
        product.slug = slugify(product.name)
        product.save()
        return product


""" CATEGORY """
""" # این مدل اولیه بود
# class CategorySerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=255)
#     description = serializers.CharField(max_length=500)
"""
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'description', 'all_products']

    all_products = serializers.IntegerField(source="products.count", read_only=True)
    """ این مدل اولیه بود
    # all_products = serializers.SerializerMethodField()
    # def get_all_products(self, category):
    #     return category.products.count()
    """



""" COMMENT """
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'name', 'body'  ]

    def create(self, validated_data):
        product_id = self.context['product_pk']
        return Comment.objects.create(product_id=product_id,**validated_data)




""" PRODUCT SERILIZIER FOR CART PAGE """
class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'unit_price']

""" CHANGE QUANTITY IN CART ITEMS """
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity', ] 



""" ADDING TO CART SERIALIZER """
class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

    def create(self, validated_data):
        cart_id = self.context['cart_pk']
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')

        """ if a product also is exists """
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product.id)
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart_id=cart_id, **validated_data)


        self.instance = cart_item
        return cart_item

        """ ANOTHER WAY for up codes """
        # if CartItem.objects.filter(cart_id=cart_id, product_id=product.id).exists():
        #     cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product.id)
        #     cart_item.quantity += quantity
        #     cart_item.save()
        # else:
        #     cart_item = CartItem.objects.create(cart_id=cart_id, **validated_data)

        # return cart_item




""" CART ITEM """
class CartItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer()
    item_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'item_total']

    def get_item_total(self, cart_item):
        return cart_item.quantity * cart_item.product.unit_price


""" CART """
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']
        read_only_fields = ['id', ]

    def get_total_price(self, cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = ['id', 'user', 'birth_date']
        read_only_fields = ['user']


class OrderItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['id', 'name', 'unit_price']

class OrderItemSerializer(serializers.ModelSerializer):
    product = OrderItemProductSerializer()
    class Meta:
        model = models.OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price']



class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = models.Order
        fields = ['id', 'customer_id', 'status', 'datetime_created', 'items']






""" # ارور داد
# products = serializers.SerializerMethodField()
# def get_products(self, category):
#     return len(Category.objects.select_related('products').all())
# print(products)
# ارور داد
# lenght_products = len(product)
# category = CategorySerializer()
# category = serializers.HyperlinkedRelatedField(
#     queryset=Category.objects.all(),
#     view_name="category-detailaaa",
# )
# id = serializers.IntegerField()
# name = serializers.CharField(max_length=255)
# inventory = serializers.IntegerField()
# -----------------------------------------------------------------
# title = serializers.CharField(max_length=255, source="name")
# price = serializers.DecimalField(max_digits=6, decimal_places=2, source="unit_price")
# price_tomans = serializers.SerializerMethodField()
    # category = serializers.StringRelatedField()
    # category = serializers.PrimaryKeyRelatedField(
    #     queryset=Category.objects.all()
    # )
    # def get_price_tomans(self, product):
    #     return int(product.unit_price * DOLLORS_TO_TOMANS)
"""