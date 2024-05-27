from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal

from store_app.models import Product, Customer, Cart, OrderPlaced, Wishlist
from payment.models import Payment


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Product.objects.create(
            title="Test Product",
            selling_price=100.00,
            discount_price=10.00,
            description="Test description",
            category="CR",
        )

    def test_price_with_discount(self):
        product = Product.objects.get(id=1)
        expected_price_with_discount = 90.00  # 100.00 - 10.00
        self.assertEqual(product.price_with_discount, expected_price_with_discount)

    def test_str_representation(self):
        product = Product.objects.get(id=1)
        expected_str = "Test Product, price: 90.0"
        self.assertEqual(str(product), expected_str)


class CustomerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username="testuser")
        Customer.objects.create(
            user=User.objects.get(username="testuser"),
            name="Test Customer",
            location="Test Location",
            city="Test City",
            phone=123456789,
            zip_code=12345,
            state="AL",
        )

    def test_str_representation(self):
        customer = Customer.objects.get(id=1)
        expected_str = "Test Customer"
        self.assertEqual(str(customer), expected_str)


class CartModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username="testuser")
        Product.objects.create(
            title="Test Product",
            selling_price=100.00,
            discount_price=10.00,
            description="Test description",
            category="CR",
        )
        Cart.objects.create(
            user=User.objects.get(username="testuser"),
            product=Product.objects.get(id=1),
            quantity=2,
        )

    def test_total_cost(self):
        cart = Cart.objects.get(id=1)
        expected_total_cost = Decimal("20.00")
        self.assertEqual(cart.total_cost, expected_total_cost)

    def test_str_representation(self):
        cart = Cart.objects.get(id=1)
        expected_str = "Cart of testuser"
        self.assertEqual(str(cart), expected_str)


class OrderPlacedModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username="testuser")
        Product.objects.create(
            title="Test Product",
            selling_price=100.00,
            discount_price=10.00,
            description="Test description",
            category="CR",
        )
        Customer.objects.create(
            user=User.objects.get(username="testuser"),
            name="Test Customer",
            location="Test Location",
            city="Test City",
            phone=123456789,
            zip_code=12345,
            state="AL",
        )
        Payment.objects.create(
            user=User.objects.get(username="testuser"),
            amount=100.00,
            order_id="Test Order ID",
            payment_status="Test Payment Status",
            payment_id="Test Payment ID",
            paid=True,
        )
        OrderPlaced.objects.create(
            user=User.objects.get(username="testuser"),
            customer=Customer.objects.get(id=1),
            product=Product.objects.get(id=1),
            quantity=2,
            status="Test Status",
            payment=Payment.objects.get(id=1),
        )

    def test_total_cost(self):
        order_placed = OrderPlaced.objects.get(id=1)
        expected_total_cost = 180.00  # 2 * 90.00
        self.assertEqual(order_placed.total_cost, expected_total_cost)

    def test_str_representation(self):
        order_placed = OrderPlaced.objects.get(id=1)
        expected_str = (
            "Order information for testuser. Status: Test Status. Payment: 100.0$"
        )
        self.assertEqual(str(order_placed), expected_str)


class WishlistModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username="testuser")
        Product.objects.create(
            title="Test Product",
            selling_price=100.00,
            discount_price=10.00,
            description="Test description",
            category="CR",
        )
        Wishlist.objects.create(
            user=User.objects.get(username="testuser"),
            product=Product.objects.get(id=1),
        )

    def test_str_representation(self):
        wishlist = Wishlist.objects.get(id=1)
        expected_str = "Wishlist of testuser with Test Product, price: 90.0"
        self.assertEqual(str(wishlist), expected_str)
