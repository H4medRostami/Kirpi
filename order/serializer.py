from rest_framework import serializers
from order.models import Order
from factor.models import Factor
from payment.models import Payment
from products.models import Products

# admin side full field CRUD operation serializer
class OrderOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


# Order Table serializer using in below as a nested serializer
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['OrderId', 'ProductId', 'Quantity']


# Base order nested serializer to get order from user and make semi final shop operation
class UserOrderSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True)

    class Meta:
        model = Factor
        fields = ['UserId', 'Description', 'UserAddress', 'orders']

    def create(self, validated_data,):
        orders = validated_data.pop('orders')
        # its for example if you have shipment policy or third-party transfer API , should be to implement this section.
        validated_data['ShipPrice'] = 12
        validated_data['ShipmentStatus'] = False

        factor = Factor.objects.create(**validated_data)
        for order in orders:
            order['Price'] = Products.objects.get(ProductId=order['ProductId'].ProductId).ProductPrice
            Order.objects.create(FactorId=factor, **order)
        Payment.objects.create(FactorId=factor, PaymentAmount=factor.total_price())
        return factor
