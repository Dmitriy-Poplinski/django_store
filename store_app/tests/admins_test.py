from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from store_app.models import Product, Customer, Cart, OrderPlaced, Wishlist


class AdminTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="password"
        )
        self.client.force_login(self.admin_user)

    def test_product_admin(self):
        response = self.client.get(reverse("admin:store_app_product_changelist"))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Products")

        product = Product.objects.create(
            title="Test Product",
            selling_price=10.00,
            discount_price=5.00,
            category="CR",
        )

        response = self.client.get(reverse("admin:store_app_product_changelist"))
        self.assertContains(response, "Test Product")

        response = self.client.get(
            reverse("admin:store_app_product_change", args=[product.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")

    def test_customer_admin(self):
        response = self.client.get(reverse("admin:store_app_customer_changelist"))
        self.assertEqual(response.status_code, 200)

    def test_cart_admin(self):
        response = self.client.get(reverse("admin:store_app_cart_changelist"))
        self.assertEqual(response.status_code, 200)

    def test_order_placed_admin(self):
        response = self.client.get(reverse("admin:store_app_orderplaced_changelist"))
        self.assertEqual(response.status_code, 200)

    def test_wishlist_admin(self):
        response = self.client.get(reverse("admin:store_app_wishlist_changelist"))
        self.assertEqual(response.status_code, 200)
