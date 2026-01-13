from django.utils.text import slugify

from decimal import Decimal

from rest_framework import serializers

from store.models import Category, Product


# این مدل اولیه بود
# class CategorySerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=255)
#     description = serializers.CharField(max_length=500)
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'description',]



# DOLLORS_TO_TOMANS = 150000
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








