import json

from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from rest_framework.views import status

from order.factories import UserFactory
from product.factories import CategoryFactory, ProductFactory
from product.models import Product


class TestProductViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory()
        token = Token.objects.create(user=self.user)
        token.save()

        self.category = CategoryFactory(title="technology")
        self.product = ProductFactory(
            title="pro controller",
            price=200.00,
            category=[self.category]  # Associa a categoria ao produto
        )
        self.product.save()  # Salva o produto com a categoria associada


    def test_get_all_product(self):
        response = self.client.get(reverse("product-list", kwargs={"version": "v1"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        product_data = json.loads(response.content)

        # Verifique se product_data é uma lista e possui elementos
        self.assertIsInstance(product_data, list)
        self.assertGreater(len(product_data), 0)

        # Verifique se o produto contém as informações esperadas
        self.assertEqual(product_data[0]["title"], self.product.title)
        self.assertEqual(product_data[0]["price"], self.product.price)
        self.assertEqual(product_data[0]["active"], self.product.active)

        # Verifique se "category" é uma lista e possui pelo menos um elemento antes de acessar
        self.assertIn("category", product_data[0])
        self.assertIsInstance(product_data[0]["category"], list)
        self.assertGreater(len(product_data[0]["category"]), 0)

        # Agora acesse "title" da primeira categoria
        self.assertEqual(
            product_data[0]["category"][0]["title"], self.category.title
        )

    def test_create_product(self):
        token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        category = CategoryFactory()
        data = json.dumps(
            {"title": "notebook", "price": 800.00,
                "categories_id": [category.id]}
        )

        response = self.client.post(
            reverse("product-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_product = Product.objects.get(title="notebook")

        self.assertEqual(created_product.title, "notebook")
        self.assertEqual(created_product.price, 800.00)