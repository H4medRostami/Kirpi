
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


router = DefaultRouter()
router.register(r'v1/father/product', ProductOperation)
router.register(r'v1/father/order', OrderOperation)
router.register(r'v1/father/factor', FactorOperation)
router.register(r'v1/father/usermanagement', UserManagement, 'usermanagement')
router.register(r'v1/father/payment', PaymentOperation)

router.register(r'v1/signup', SignUp, 'signup',)
router.register(r'v1/myprofile', MyProfile, 'myprofile')
router.register(r'v1/editprofile', EditMyProfile, 'editprofile')
router.register(r'v1/productlist', ProductList)
router.register(r'v1/paymentlist', PaymentList, 'paymentlist')
router.register(r'v1/order', UserOrder, 'order')


urlpatterns = [
        url(r'^v1/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('', include(router.urls)),

        path('v1/api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('v1/api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

