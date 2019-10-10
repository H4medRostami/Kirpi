import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from authentication.tests.test_jwt import AuthenticationTest
from rest_framework.test import APITestCase
from rest_framework.test import APIClient


class AuthenticationAppTest(AuthenticationTest, APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='hamed', password='234')
        self.user.save()
        # signUp reverse url:
        self.signup_url = reverse('signup-list')
        # MyProfile reverse url:
        self.my_profile_url = reverse('my_profile-list')
        # EditMyProfile reverse url:
        self.edit_my_profile_url = reverse('edit_my_profile-detail', kwargs={'pk': self.user.pk})
        # UserManagement reverse urls:
        self.create_read_url = reverse('user_operation-list')
        self.read_update_delete_url = reverse('user_operation-detail', kwargs={'pk': self.user.pk})




        # if you want use force authenticate:
        self.me = super().setUp()
        self.client = APIClient()
        self.client.force_authenticate(user=self.me)

        # if want to use by token call use like below:
        # super().test_api_jwt()
        # self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.tkn['access'])
    # client sign up
    def test_signup(self):
        """ sign up new user
            Method : POST
            Permission : AnyOne
            Authentication : Anyone
        """
        data = {'username': 'test1',
                'password': 'test'}

        response = self.client.post(self.signup_url, data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    # render client's profile
    def test_my_profile(self):
        """ Fetch current User record over PK
            Method : GET/PK/
            Permission : IsAdmin
            Authentication : IsAuthenticated
        """
        response = self.client.get(self.my_profile_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['username'], self.me.username)

    # Edit client's profile
    def test_edit_my_profile(self):
        """ Get current User record
            Method : GET/PK/
            Permission : Anyone
            Authentication : IsAuthenticated
        """
        content = {'email': 'testuser@test.com'}
        response = self.client.patch(self.edit_my_profile_url, content)
        self.assertEquals(response.data['username'], self.me.username)

    # admin control over users
    def test_user_management_list(self):
        """ Get users list
            Method : GET
            Permission : IsAdmin
            Authentication : IsAuthenticated
        """
        response = self.client.get(self.create_read_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(User.objects.count(), 2)

    def test_user_management_create(self):
        """ Create new User record
            Method : POST
            Permission : IsAdmin
            Authentication : IsAuthenticated
        """
        post = {'username': 'test2',
                'password': 'test2',
                'email': 'test2@test.com'}
        response = self.client.post(self.create_read_url, post)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.data['username'], 'test2')

    def test_user_management_detail(self):
        """ Get User record over PK
            Method : GET/PK/
            Permission : IsAdmin
            Authentication : IsAuthenticated
        """
        response = self.client.get(self.read_update_delete_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['username'], self.user.username)

    def test_user_management_update(self):
        """ Update User record over PK
            Method : PUT/PK/
            Permission : IsAdmin
            Authentication : IsAuthenticated
        """
        data = {'username': 'hasan',
                'password': 'hasan34',
                'email': 'hasan@test.com'}
        response = self.client.put(self.read_update_delete_url, data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'hasan')

    def test_user_management_partial_update(self):
        """ Partial update User record over PK
            Method : PATCH/PK/
            Permission : IsAdmin
            Authentication : IsAuthenticated
        """
        data = {'username': 'ziya'}
        response = self.client.patch(self.read_update_delete_url, data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'ziya')

    def test_user_management_delete(self):
        """ Delete User record over PK
            Method : DELETE/PK/
            Permission : IsAdmin
            Authentication : IsAuthenticated
        """
        response = self.client.delete(self.read_update_delete_url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response.data)
