
from factor.models import Factor
from factor.serializer import FactorSerializer
from rest_framework import throttling
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions


# admin side CRUD operation view set
class FactorOperation(ModelViewSet):
    throttle_classes = [throttling.AnonRateThrottle]
    permission_classes = (permissions.IsAdminUser, permissions.IsAuthenticated)
    serializer_class = FactorSerializer
    queryset = Factor.objects.all()



