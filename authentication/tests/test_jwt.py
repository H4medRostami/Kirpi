from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class AuthenticationTest(APITestCase):
    # pass token to APIs to authentication .
    tkn = {}

    def setUp(self):
        u = User.objects.create_superuser(username='test', email='test@test.com', password='test')
        u.save()
        return u

    def test_api_jwt(self):
        """ pass  username and password to get access and refresh token.
                    Method : POST
                    Permission : AnyOne
                    Authentication : AnyOne
        """
        url = reverse('token_obtain_pair')

        self.resp = self.client.post(url, {'username': 'test', 'password': 'test'}, format='json')

        self.assertEquals(self.resp.status_code, status.HTTP_200_OK)
        self.tkn = self.resp.data