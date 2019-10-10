from rest_framework import serializers
from products.models import Products


# serializer using in admin and user side
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['ProductId', 'ProductName', 'ProductQuantity', 'ProductPrice', 'ProductDescription']
