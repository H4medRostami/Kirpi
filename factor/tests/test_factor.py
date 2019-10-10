from django.urls import reverse
from rest_framework import status
from authentication.tests.test_jwt import AuthenticationTest
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from factor.models import Factor


class FactorAppTest(AuthenticationTest, APITestCase):

    def setUp(self):

        # if you want use force authenticate:
        self.me = super().setUp()
        self.client = APIClient()
        self.client.force_authenticate(user=self.me)

        # if want to use by token call, use like below:
        # super().test_api_jwt()
        # self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.tkn['access'])

        self.factor = Factor.objects.create(Description='XYZ',
                                                          UserAddress='T234',
                                                          ShipPrice=85.2,
                                                          UserId=self.me)

        self.factor.save()
        # Factor management urls:
        self.create_read_url = reverse('factor_operation-list')
        self.read_partial_delete_url = reverse('factor_operation-detail', kwargs={'pk': self.factor.FactorId})

    # admin control over Factor:
    def test_factor_list(self):
        """ render factors list
            Method : GET
            Permission : IsAdmin
            Authentication : IsAuthenticated
        """
        response = self.client.get(self.create_read_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_factor_create(self):
        """ create new factor
            Method : POST
            Permission : IsAdmin
            Authentication : IsAuthenticated
        """
        post = {'Description': 'XYZ',
                'UserAddress': 'T234',
                'ShipPrice': 85.2,
                'UserId': self.me.pk}

        response = self.client.post(self.create_read_url, post)
        self.assertEquals(response.status_code, 201)

    def test_factor_detail(self):
        """ Get factor over FactorId as PK
            Method : GET/PK/
            Permission : IsAdmin
            Authentication : IsAuthenticated
        """
        response = self.client.get(self.read_partial_delete_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_factor_update(self):
        """ Update factor record over FactorId ad PK
            Method : PUT/PK/
            Permission : IsAdmin
            Authentication : IsAuthenticated
        """
        data = {'Description': 'XYZe',
                'UserAddress': 'Tw234',
                'ShipPrice': 86.2,
                'UserId': self.me.pk}

        response = self.client.put(self.read_partial_delete_url, data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_factor_partial_update(self):
        """ Particular update factor record over FactorId ad PK
            Method : PATCH/PK/
            Permission : IsAdmin
            Authentication : IsAuthenticated
        """
        data = {'Description': 'please send in Gift packet'}

        response = self.client.patch(self.read_partial_delete_url, data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_factor_delete(self):
        """ Delete factor record over FactorId as PK
            Method : DELETE/PK/
            Permission : IsAdmin
            Authentication : IsAuthenticated
        """
        response = self.client.delete(self.read_partial_delete_url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)



