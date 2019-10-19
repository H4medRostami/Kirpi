
from order.models import Order
from factor.models import Factor
from order.serializer import OrderSerializer, UserOrderSerializer, OrderOperationSerializer
from rest_framework import throttling, status
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from django.db import connection


def user_failed_shops(current_user):
    user = int(current_user)
    with connection.cursor() as cursor:
        cursor.execute(f''' select count(*) 
                            from public.factor_factor
                            inner join public.payment_payment on public.factor_factor."FactorId" = public.payment_payment."FactorId_id"
                            where public.factor_factor."UserId_id"={user} and public.payment_payment."PaymentStatus"=FALSE;''')
        row = cursor.fetchone()
    return row[0]


class OrderOperation(ModelViewSet):
    throttle_classes = [throttling.AnonRateThrottle]
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OrderOperationSerializer
    queryset = Order.objects.all()


class UserOrder(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer(self):
        return UserOrderSerializer()

    def create(self, request):
        serializer = UserOrderSerializer(data=request.data)
        result = user_failed_shops(request.user.id)
        # limit un_success payment to 5 times. its example to punish butterfly clients .
        if result >= 5:
            return Response("Unfortunately you reached unsuccess Payment quota!", status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save(UserId=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Factor.objects.filter(UserId=self.request.user.id)
        serializer = UserOrderSerializer(queryset, many=True)
        return Response(serializer.data)
