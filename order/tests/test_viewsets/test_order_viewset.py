import json

from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from order.factories import OrderFactory, UserFactory
from product.factories import CategoryFactory, ProductFactory
from order.models import Order


class TestOrderViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory()
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        self.category = CategoryFactory(title="technology")
        self.product = ProductFactory(
            title="mouse", price=100, category=[self.category]
        )
        self.order = OrderFactory(product=[self.product], user=self.user)

    def test_order(self):
        response = self.client.get(reverse("order-list", kwargs={"version": "v1"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_data = json.loads(response.content)

        # Validação dos dados do pedido
        self.assertIn("results", order_data)
        self.assertEqual(order_data["results"][0]["product"][0]["title"], self.product.title)
        self.assertEqual(order_data["results"][0]["product"][0]["price"], self.product.price)
        self.assertEqual(order_data["results"][0]["product"][0]["active"], self.product.active)
        self.assertEqual(order_data["results"][0]["product"][0]["category"][0]["title"], self.category.title)

    def test_create_order(self):
        # Configuração do token de autenticação
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        data = json.dumps({
            "products_id": [self.product.id],
            "user": self.user.id
        })

        response = self.client.post(
            reverse("order-list", kwargs={"version": "v1"}),
        )