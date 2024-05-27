from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from decimal import Decimal

from store_app.models import Cart, Product, Wishlist
from store_app.utils.utils import (
    total_wishlist_items_util,
    change_amount_carts_util,
    change_cart_quantity_util,
)


class UtilsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        self.product = Product.objects.create(
            title="Product 1",
            category="fruits",
            selling_price=Decimal("10.99"),
            discount_price=Decimal("1.99"),
            product_image="test_image.png",
        )

    def test_total_wishlist_items_util_authenticated_user(self):
        request = self.factory.get("/")
        request.user = self.user
        cart = Cart.objects.create(user=self.user, product=self.product, quantity=2)
        wishlist = Wishlist.objects.create(user=self.user, product=self.product)

        total_item, wishlist_item = total_wishlist_items_util(request)

        self.assertEqual(total_item, 1)
        self.assertEqual(wishlist_item, 1)

    def test_total_wishlist_items_util_unauthenticated_user(self):
        request = self.factory.get("/")
        request.user = AnonymousUser()

        total_item, wishlist_item = total_wishlist_items_util(request)

        self.assertEqual(total_item, 0)
        self.assertEqual(wishlist_item, 0)

    def test_change_amount_carts_util_return_json(self):
        request = self.factory.get("/")
        request.user = self.user
        cart = Cart.objects.create(user=self.user, product=self.product, quantity=2)

        result = change_amount_carts_util(request, cart, return_type="json")

        self.assertIsInstance(result, dict)
        self.assertIn("quantity", result)
        self.assertIn("total_amount", result)
        self.assertIn("amount", result)

    def test_change_amount_carts_util_return_request(self):
        request = self.factory.get("/")
        request.user = self.user
        Cart.objects.create(user=self.user, product=self.product, quantity=2)

        carts, total_amount = change_amount_carts_util(request, return_type="req")

        self.assertIsInstance(carts.first(), Cart)
        self.assertIsInstance(total_amount, float)

    def test_change_cart_quantity_util(self):
        request = self.factory.get("/", {"product_id": self.product.pk})
        request.user = self.user
        cart = Cart.objects.create(user=self.user, product=self.product, quantity=2)

        updated_cart = change_cart_quantity_util(request, quantity=1)

        self.assertEqual(updated_cart.quantity, 3)
