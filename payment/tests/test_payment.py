from django.urls import reverse
from rest_framework import status
from authentication.tests.test_jwt import AuthenticationTest
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from payment.models import Payment
from factor.models import Factor


class PaymentAppTest(AuthenticationTest, APITestCase):

    def setUp(self):
        # if you want use force authenticate:
        self.me = super().setUp()
        self.client = APIClient()
        self.client.force_authenticate(user=self.me)

        # if want to use by token call use like below:
        # super().test_api_jwt()
        # self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.tkn['access'])

        self.factor = Factor.objects.create(Description='XYZ', UserAddress='T234', ShipPrice=23.2, UserId=self.me)
        self.payment = Payment.objects.create(PaymentAmount=2, PaymentStatus=True, FactorId=self.factor)
        self.payment.save()
        # User payments reverse urls:
        self.user_create_read_url = reverse('my_payment_list-list')
        # Payments Management reverse urls:
        self.create_read_url = reverse('payment_operation-list')
        self.read_update_delete_url = reverse('payment_operation-detail', kwargs={'pk': self.payment.PaymentId})
    # user payments list shown to user:
    def test_user_payment_list(self):
        """ render product list for clients
            Method : GET
            Permission : AnyOne
            Authentication : IsAuthenticated
        """

        response = self.client.get(self.user_create_read_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    # admin control over payments :
    def test_payment_list(self):
        """ render payments list
            Method : GET
            Permission : IsAdmin
            Authentication : IsAuthenticated
        """
        response = self.client.get(self.create_read_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_user_payment_create(self):
        """ create new payment
            Method : POST
            Permission : IsAdmin
            Authentication : IsAuthenticated
        """
        data = {'PaymentAmount': 3,
                'PaymentStatus': True,
                'FactorId': self.factor.FactorId}

        response = self.client.post(self.create_read_url, data=data)
        self.assertEquals(response.status_code, 201)

    def test_user_payment_detail(self):
        """ Get payment over PaymentId as PK
            Method : GET/PK/
            Permission : IsAdmin
            Authentication : IsAuthenticated
        """
        response = self.client.get(self.read_update_delete_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['PaymentId'], self.payment.PaymentId)

    def test_user_payment_update(self):
        """ Update Payment record over PaymentId as PK
            Method : PUT/PK/
            Permission : IsAdmin
            Authentication : IsAuthenticated
        """
        data = {'PaymentAmount': 3.25,
                'PaymentStatus': True,
                'FactorId': self.factor.FactorId}

        response = self.client.put(self.read_update_delete_url, data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['PaymentAmount'], data['PaymentAmount'].__str__())

    def test_user_payment_partial_update(self):
        """ Partial update payment record  over PaymentId ad PK
            Method : PATCH/PK/
            Permission : IsAdmin
            Authentication : IsAuthenticated
        """
        data = {'PaymentAmount': 3.65}
        response = self.client.patch(self.read_update_delete_url, data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['PaymentAmount'], data['PaymentAmount'].__str__())

    def test_user_payment_delete(self):
        """ Delete payment record over PaymentId as PK
            Method : DELETE/PK/
            Permission : IsAdmin
            Authentication : IsAuthenticated
        """
        response = self.client.delete(self.read_update_delete_url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response.data)

