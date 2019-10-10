
from order.models import Order
from factor.models import Factor
from order.serializer import OrderSerializer, UserOrderSerializer, OrderOperationSerializer
from rest_framework import throttling, status
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, viewsets
from rest_framework.response import Response


class OrderOperation(ModelViewSet):
    throttle_classes = [throttling.AnonRateThrottle]
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OrderOperationSerializer
    queryset = Order.objects.all()


class UserOrder(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request):
        serializer = UserOrderSerializer(data=request.data)
        result = Factor.objects.filter(UserId__factor__payment=self.request.user.id).count()
        # todo: limit unsuccess paymanent to 5 times.
        if result >= 5:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save(UserId=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Factor.objects.filter(UserId=self.request.user.id)
        serializer = UserOrderSerializer(queryset, many=True)
        return Response(serializer.data)
