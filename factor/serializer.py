from rest_framework import serializers
from factor.models import Factor


# admin side CRUD operation serializer
class FactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factor
        fields = ['FactorId', 'Description', 'UserAddress', 'UserId', 'ShipmentStatus', 'ShipPrice', 'OrderDate']



