from django.urls import reverse
from rest_framework import status
from authentication.tests.test_jwt import AuthenticationTest
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from products.models import Products


class ProductAppTest(AuthenticationTest, APITestCase):

    def setUp(self):
        self.product = Products.objects.create(ProductName='shoe', ProductQuantity=2,
                                               ProductPrice=2.12, ProductDescription='Tabriz shoes')
        self.product.save()

        # product management urls:
        self.create_read_url = reverse('product_operation-list')
        self.read_update_delete_url = reverse('product_operation-detail', kwargs={'pk': self.product.ProductId})

        # Products Management reverse urls:
        self.user_create_read_url = reverse('product_list-list')

        # if you want use force authenticate:
        self.me = super().setUp()
        self.client = APIClient()
        self.client.force_authenticate(user=self.me)

        # if want to use by token call use like below:
        # super().test_api_jwt()
        # self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.tkn['access'])
    # client side {fetch products list in clients endpoints}
    def test_user_product_list(self):
        """ render product list for clients
            Method : GET
            Permission : AnyOne
            Authentication : None
        """

        response = self.client.get(self.user_create_read_url)
        self.assertContains(response, self.product.ProductDescription)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    # Admin side control over products:
    def test_product_list(self):
        """ render products list
            Method : GET
            Permission : IsAdmin
            Authentication : IsAuthenticated
        """
        response = self.client.get(self.create_read_url)
        self.assertContains(response, self.product.ProductDescription)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_product_create(self):
        """ create new product
            Method : POST
            Permission : IsAdmin
            Authentication : IsAuthenticated

         """

        post = {
            "ProductName": "hat",
            "ProductQuantity": 5,
            "ProductPrice": 2.12,
            "ProductDescription": "fedora hat"
        }

        response = self.client.post(self.create_read_url, post)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.data['ProductName'], post['ProductName'])

    def test_product_detail(self):
        """ get product over ProductId as PK
            Method : GET/PK/
            Permission : IsAdmin
            Authentication : IsAuthenticated

        """

        response = self.client.get(self.read_update_delete_url)
        self.assertEquals(response.data['ProductName'], self.product.ProductName)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_product_update(self):
        """ Update product record over ProductId as PK
            Method : PUT/PK/
            Permission : IsAdmin
            Authentication : IsAuthenticated

        """

        data = {
            "ProductName": "book",
            "ProductQuantity": 8,
            "ProductPrice": 3.12,
            "ProductDescription": "programing book"
        }
        response = self.client.put(self.read_update_delete_url, data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, data['ProductName'])

    def test_product_partial_update(self):
        """ Particular update product record over ProductId as PK
            Method : PATCH/PK/
            Permission : IsAdmin
            Authentication : IsAuthenticated
        """

        data = {
            "ProductName": "pencil",
            }
        response = self.client.patch(self.read_update_delete_url, data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_product_delete(self):
        """ Delete product record according ProductId as PK
            Method : DELETE/PK/
            Permission : IsAdmin
            Authentication : IsAuthenticated
        """

        response = self.client.delete(self.read_update_delete_url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response.data)



