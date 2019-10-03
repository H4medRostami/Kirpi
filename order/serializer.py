from rest_framework import serializers
from order.models import Order
from factor.models import Factor
from payment.models import Payment


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['OrderId', 'ProductId', 'Quantity', 'Price', 'FactorId']


class UserOrderSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True)

    class Meta:
        model = Factor
        fields = ['UserId', 'Description', 'UserAddress', 'orders']

    def create(self, validated_data,):
        orders = validated_data.pop('orders')
        validated_data['ShipPrice'] = 12
        validated_data['ShipmentStatus'] = False
        factor = Factor.objects.create(**validated_data)
        for order in orders:
            Order.objects.create(FactorId=factor, **order)
        Payment.objects.create(FactorId=factor, PaymentAmount=factor.total_price())
        return factor
