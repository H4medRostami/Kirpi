from django.test import TestCase
from django.urls import reverse


class SignUpTest(TestCase):
    def setUp(self):
        self.post = reverse('signup-list')

    def test_create(self):
        post = {'username': 'test', 'password': 'test'}
        response = self.client.post(self.post, post)
        self.assertEquals(response.status_code, 201)
