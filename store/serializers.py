from rest_framework import serializers


DOLLORS_TO_TOMANS = 150000


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255, source="name")
    name = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source="unit_price")
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    inventory = serializers.IntegerField()
    price_tomans = serializers.SerializerMethodField()

    def get_price_tomans(self, product):
        return int(product.unit_price )



