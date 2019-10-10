from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from payment.models import Payment
from payment.serializer import PaymentSerializer
from rest_framework import throttling
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from factor.models import Factor


# Pagination class using for divide rendering 100 per page
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    # page_size_query_param = 'page_size'
    # max_page_size = 1000


# Admin side CRUD operation
class PaymentOperation(ModelViewSet):
    pagination_class = StandardResultsSetPagination
    throttle_classes = [throttling.AnonRateThrottle]
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


# Client side view set
class PaymentList(viewsets.ViewSet):
    """Fetch current user payments list"""
    pagination_class = StandardResultsSetPagination
    throttle_classes = [throttling.AnonRateThrottle]
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request):
        user = Factor.objects.filter(UserId=self.request.user.id)
        queryset = Payment.objects.filter(FactorId__in=user)
        serializer = PaymentSerializer(queryset, many=True, read_only=True)
        return Response(serializer.data)

