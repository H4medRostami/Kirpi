import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UserManagementTests(TestCase):
    def setUp(self):
        User.objects.get_or_create(username='test', password='test')
        User.objects.get_or_create(username='test1', password='test1')
        self.create_read_url = reverse('usermanagement-list')
       # self.read_update_delete_url = \
         #   reverse('usermanagement-detail', args='1')

    def test_list(self):
        response = self.client.get(self.create_read_url,HTTP_AUTHORIZATION)
        # Are both titles in the content?
        self.assertContains(response, 'test1')
        self.assertContains(response, 'test2')
"""
    def test_detail(self):
        response = self.client.get(self.read_update_delete_url)
        data = json.loads(response.content)
        content = {'id': 1, 'title': 'title1', 'slug': 'slug1', 'scoops_remaining': 0}
        self.assertEquals(data, content)

    def test_create(self):
        post = {'title': 'title3', 'slug': 'slug3'}
        response = self.client.post(self.create_read_url, post)
        data = json.loads(response.content)
        self.assertEquals(response.status_code, 201)
        content = {'id': 3, 'title': 'title3', 'slug': 'slug3',
                   'scoops_remaining': 0}
        self.assertEquals(data, content)
        self.assertEquals(Flavor.objects.count(), 3)

    def test_delete(self):
        response = self.client.delete(self.read_update_delete_url)

        self.assertEquals(response.status_code, 204)
        self.assertEquals(Flavor.objects.count(), 1)
"""