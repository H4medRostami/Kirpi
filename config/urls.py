
from django.conf.urls import url
from authentication.views import SignUp, UserManagement, MyProfile, EditMyProfile
from products.views import ProductOperation, ProductList
from order.views import OrderOperation, UserOrder
from factor.views import FactorOperation
from payment.views import PaymentList, PaymentOperation
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from swagger import schema_view
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

# DRF Default router
router = DefaultRouter()
# client side urls :
router.register(r'v1/father/products', ProductOperation, 'product_operation')
router.register(r'v1/father/orders', OrderOperation, 'order_operation')
router.register(r'v1/father/factors', FactorOperation, 'factor_operation')
router.register(r'v1/father/users', UserManagement, 'user_operation')
router.register(r'v1/father/payments', PaymentOperation, 'payment_operation')
# admin side urls :
router.register(r'v1/signup', SignUp, 'signup',)
router.register(r'v1/myprofile', MyProfile, 'my_profile')
router.register(r'v1/editprofile', EditMyProfile, 'edit_my_profile')
router.register(r'v1/productlist', ProductList, 'product_list')
router.register(r'v1/paymentlist', PaymentList, 'my_payment_list')
router.register(r'v1/order', UserOrder, basename='order')

urlpatterns = [
        url(r'^v1/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('', include(router.urls)),

        url(r'^v1/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
        path('v1/api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('v1/api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

