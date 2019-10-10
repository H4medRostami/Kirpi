from rest_framework.pagination import PageNumberPagination

from products.models import Products
from products.serializer import ProductSerializer
from rest_framework import status, throttling
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins


# Pagination class 100 per page
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    # page_size_query_param = 'page_size'
    # max_page_size = 1000


# Admin CRUD operation
class ProductOperation(ModelViewSet):

    pagination_class = StandardResultsSetPagination
    throttle_classes = [throttling.AnonRateThrottle]
    permission_classes = (permissions.IsAuthenticated,permissions.IsAdminUser)
    serializer_class = ProductSerializer
    queryset = Products.objects.all()


# Client side view set  using to fetch products in clients like Web and smartphone app.
class ProductList(mixins.ListModelMixin, GenericViewSet):

    pagination_class = StandardResultsSetPagination
    throttle_classes = [throttling.AnonRateThrottle]
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProductSerializer
    queryset = Products.objects.all()
