import json
from django.urls import reverse
from rest_framework import status
from authentication.tests.test_jwt import AuthenticationTest
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from products.models import Products
from order.models import Order


class OrderAppTest(AuthenticationTest, APITestCase):

    def setUp(self):
        self.me = super().setUp()
        self.client = APIClient()
        # if you want use force authenticate:
        self.client.force_authenticate(user=self.me)

        self.product = Products.objects.create(ProductName='shoe',
                                               ProductQuantity=2,
                                               ProductPrice=2.12,
                                               ProductDescription='Tabriz shoes')
        self.product.save()

        self.order = Order.objects.create(ProductId=self.product, Quantity=3, Price=3)
        self.order.save()
        # User order reverse urls:
        self.user_create_read_url = reverse('order-list')
        self.user_read_update_delete_url = reverse('order-detail', kwargs={'pk': self.me.pk})
        # admin order management urls:
        self.read_update_delete_url = reverse('order_operation-detail', args=[self.order.OrderId])
        self.read_create_url = reverse('order_operation-list')
        # if want to use by token call, use like below:
        # super().test_api_jwt()
        # self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.tkn['access'])

    def test_user_order_list(self):
        """ Get user orders
            Method : GET
            Permission : AnyOne
            Authentication : IsAuthenticated
        """
        response = self.client.get(self.user_read_update_delete_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_user_order_create(self):
        """  order by user
             Method : POST
             Permission : AnyOne
             Authentication : IsAuthenticated
        """

        data = {"UserId": self.me.pk,
                "Description": "make good packet",
                "UserAddress": "king house 12 ave. 352",
                "orders":
                    [{"ProductId": self.product.ProductId,
                      "Quantity": 1
                      }

                     ]
                }
        response = self.client.post(self.user_create_read_url, data=json.dumps(data), content_type='application/json')
        self.assertEquals(response.status_code, 201)

    # Admin control over order
    def test_orders_list(self):
        """ Get orders list
            Method : Get
            Permission : IsAdmin
            Authentication : IsAuthenticated
        """
        response = self.client.get(self.read_create_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_orders_create(self):
        """ create order
            Method : POST
            Permission : IsAdmin
            Authentication : IsAuthenticated
        """
        data = {'ProductId': self.product.ProductId, 'Quantity': 9, 'Price': 130}
        response = self.client.post(self.read_create_url, data=data)
        print(response.data)
        self.assertEquals(response.status_code, 201)

    def test_orders_detail(self):
        """ Get orders by OrderId
            Method : GET/PK/
            Permission : IsAdmin
            Authentication : IsAuthenticated
        """
        response = self.client.get(self.read_update_delete_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['OrderId'], self.order.OrderId)

    def test_order_update(self):
        """ update order record by OrderId
            Method : PUT
            Permission : IsAdmin
            Authentication : IsAuthenticated
        """
        data = {'ProductId': self.product.ProductId, 'Quantity': 8, 'Price': 25.56}
        response = self.client.put(self.read_update_delete_url, data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['Quantity'], data['Quantity'])

    def test_order_partial_update(self):
        """ Partial update order record by OrderId
            Method : PATCH
            Permission : IsAdmin
            Authentication : IsAuthenticated
        """
        data = {'Quantity': 3}
        response = self.client.patch(self.read_update_delete_url, data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['Quantity'], data['Quantity'])

    def test_order_delete(self):
        """ Delete order record by OrderId
            Method : DELETE
            Permission : IsAdmin
            Authentication : IsAuthenticated
        """
        response = self.client.delete(self.read_update_delete_url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response.data)
