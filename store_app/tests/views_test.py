from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.messages import get_messages
from decimal import Decimal

from store_app.forms import CustomerRegistrationForm, CustomerProfileForm
from store_app.models import Customer, Product, Wishlist, Payment, Cart, OrderPlaced


class HomeAboutContactViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

    def test_home_view(self):
        response = self.client.get(reverse("store_app:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/home.html")

    def test_about_view(self):
        response = self.client.get(reverse("store_app:about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/about.html")

    def test_contact_view(self):
        response = self.client.get(reverse("store_app:contact"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/contact.html")


class CategoryViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

        self.category_name = "test_category"
        self.product_title = "Test Product"
        self.product_selling_price = Decimal("10.99")
        self.product_discount_price = Decimal("1.99")
        self.product_image = "static/app/images/product/icbars.png"

        self.product = Product.objects.create(
            title=self.product_title,
            category=self.category_name,
            selling_price=self.product_selling_price,
            discount_price=self.product_discount_price,
            product_image=self.product_image,
        )

    def test_category_view(self):
        url = reverse("store_app:category", kwargs={"name": self.category_name})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/category.html")
        self.assertContains(response, self.product_title)


class CategoryTitleViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

        self.category_name = "Test Category"
        self.product_title = "Test Product"
        self.product_selling_price = Decimal("10.99")
        self.product_discount_price = Decimal("1.99")
        self.product_image = "static/app/images/product/icbars.png"

        self.product = Product.objects.create(
            title=self.product_title,
            category=self.category_name,
            selling_price=self.product_selling_price,
            discount_price=self.product_discount_price,
            product_image=self.product_image,
        )

    def test_category_title_view(self):
        url = reverse("store_app:category-title", kwargs={"name": self.product_title})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/category.html")
        self.assertContains(response, self.product_title)


class ProductDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.factory = RequestFactory()

        self.category_name = "Test Category"
        self.product_title = "Test Product"
        self.product_selling_price = Decimal("10.99")
        self.product_discount_price = Decimal("1.99")
        self.product_image = "static/app/images/product/icbars.png"

        self.product = Product.objects.create(
            title=self.product_title,
            category=self.category_name,
            selling_price=self.product_selling_price,
            discount_price=self.product_discount_price,
            product_image=self.product_image,
        )

        self.wishlist = Wishlist.objects.create(user=self.user, product=self.product)

    def test_product_detail_view(self):
        self.client.login(username="testuser", password="testpassword")
        url = reverse("store_app:product-detail", kwargs={"pk": self.product.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/product_detail.html")
        self.assertEqual(response.context["product"], self.product)

        wishlist_from_db = response.context["wishlist"].first()
        self.assertEqual(wishlist_from_db, self.wishlist)


class CustomerRegistrationViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_request(self):
        url = reverse("register")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/customer_registration.html")
        self.assertIsInstance(response.context["form"], CustomerRegistrationForm)

    def test_post_request_valid_data(self):
        url = reverse("register")
        data = {
            "email": "test@email.com",
            "username": "testusername",
            "password1": "1997test1997",
            "password2": "1997test1997",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/customer_registration.html")

        self.assertTrue(User.objects.filter(username="testusername").exists())

        messages = [str(msg) for msg in get_messages(response.wsgi_request)]
        self.assertIn("Congratulations! User registered successfully!", messages)

    def test_post_request_invalid_data(self):
        url = reverse("register")
        data = {}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/customer_registration.html")

        self.assertTrue(response.context["form"].errors)

        messages = [str(msg) for msg in get_messages(response.wsgi_request)]
        self.assertIn("Invalid input data, please try again.", messages)


class CustomerProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")
        self.product_selling_price = Decimal("10.99")

    def test_profile_view_get(self):
        response = self.client.get(reverse("store_app:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/profile.html")

    def test_profile_view_post(self):
        form_data = {
            "name": "John Doe",
            "location": "123 Main St",
            "city": "Anytown",
            "phone": "1234567890",
            "state": "AZ",
            "zip_code": "12345",
        }

        response = self.client.post(reverse("store_app:profile"), data=form_data)

        form = CustomerProfileForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")

        self.assertEqual(Customer.objects.count(), 1)
        customer = Customer.objects.first()
        self.assertEqual(customer.name, "John Doe")

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Your profile has been saved successfully!")


class AddressViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")
        self.address = Customer.objects.create(
            user=self.user,
            name="John Doe",
            location="Some Address",
            city="Some City",
            phone="123456789",
            state="AZ",
            zip_code="12345",
        )

    def test_address_view(self):
        url = reverse("store_app:address")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/address.html")
        self.assertIn(self.address, response.context["addresses"])


class UpdateAddressViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")
        self.address = Customer.objects.create(
            user=self.user,
            name="John Doe",
            location="Some Address",
            city="Some City",
            phone="123456789",
            state="AZ",
            zip_code="12345",
        )

    def test_get_update_address_view(self):
        url = reverse("store_app:update-address", kwargs={"pk": self.address.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/update_address.html")
        self.assertEqual(response.context["form"].instance, self.address)

    def test_post_update_address_view(self):
        url = reverse("store_app:update-address", kwargs={"pk": self.address.pk})
        data = {
            "name": "Updated Name",
            "location": "Updated Address",
            "city": "Updated City",
            "phone": "987654321",
            "state": "AL",
            "zip_code": "54321",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        updated_address = Customer.objects.get(pk=self.address.pk)
        self.assertEqual(updated_address.name, "Updated Name")
        self.assertEqual(updated_address.location, "Updated Address")
        self.assertEqual(updated_address.city, "Updated City")
        self.assertEqual(updated_address.phone, 987654321)
        self.assertEqual(updated_address.state, "AL")
        self.assertEqual(updated_address.zip_code, 54321)
        messages = [str(msg) for msg in get_messages(response.wsgi_request)]
        self.assertIn("Your profile has been updated successfully!", messages)


class CheckoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")
        self.address = Customer.objects.create(
            user=self.user,
            name="John Doe",
            location="Some Address",
            city="Some City",
            phone="123456789",
            state="AZ",
            zip_code="12345",
        )

    def test_get_checkout_view(self):
        url = reverse("store_app:checkout")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/checkout.html")
        self.assertIn("addresses", response.context)
        self.assertIn("carts", response.context)
        self.assertIn("total_amount", response.context)

    def test_post_checkout_view(self):
        url = reverse("store_app:checkout")
        data = {"total_amount": "100.00", "customer_id": self.address.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Payment.objects.filter(amount="100.00").exists())
        messages = [str(msg) for msg in get_messages(response.wsgi_request)]
        self.assertIn("Your order has been created successfully!", messages)


class CartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

        self.category_name = "Test Category"
        self.product_title = "Test Product"
        self.product_selling_price = Decimal("10.99")
        self.product_discount_price = Decimal("1.99")
        self.product_image = "static/app/images/product/icbars.png"

        self.product = Product.objects.create(
            title=self.product_title,
            category=self.category_name,
            selling_price=self.product_selling_price,
            discount_price=self.product_discount_price,
            product_image=self.product_image,
        )

    def test_add_to_cart(self):
        url = reverse("store_app:add-to-cart")
        response = self.client.get(url, {"product_id": self.product.pk})
        self.assertEqual(response.status_code, 302)

    def test_show_cart(self):
        url = reverse("store_app:show-cart")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_plus_cart(self):
        cart = Cart.objects.create(user=self.user, product=self.product)
        print("Cart", Cart.objects.all())
        url = reverse("store_app:plus-cart")
        response = self.client.get(url, {"product_id": self.product.pk})
        self.assertEqual(response.status_code, 200)

    def test_minus_cart(self):
        cart = Cart.objects.create(user=self.user, product=self.product)
        print("Cart", Cart.objects.all())
        url = reverse("store_app:minus-cart")
        response = self.client.get(url, {"product_id": self.product.pk})
        self.assertEqual(response.status_code, 200)

    def test_remove_cart(self):
        cart = Cart.objects.create(user=self.user, product=self.product)

        url = reverse("store_app:remove-cart")
        response = self.client.get(url, {"product_id": self.product.pk})
        self.assertEqual(response.status_code, 200)


class OrdersViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

        self.customer = Customer.objects.create(
            user=self.user,
            name="John Doe",
            location="Some Address",
            city="Some City",
            phone="123456789",
            state="AZ",
            zip_code="12345",
        )

        self.category_name = "Test Category"
        self.product_title = "Test Product"
        self.product_selling_price = Decimal("10.99")
        self.product_discount_price = Decimal("1.99")
        self.product_image = "static/app/images/product/icbars.png"

        self.payment = Payment.objects.create(
            user=self.user,
            amount="10",
            order_id="222",
            payment_status="pending",
            payment_id="6",
        )

        self.product = Product.objects.create(
            title=self.product_title,
            category=self.category_name,
            selling_price=self.product_selling_price,
            discount_price=self.product_discount_price,
            product_image=self.product_image,
        )

        OrderPlaced.objects.create(
            user=self.user,
            status="Pending",
            quantity=100,
            user_id=self.user.id,
            customer_id=self.customer.pk,
            product_id=self.product.pk,
            payment_id=self.payment.id,
        )

    def test_orders_view(self):
        url = reverse("store_app:orders")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Pending")
        self.assertNotContains(response, "Shipped")
        self.assertNotContains(response, "Delivered")


class SearchViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

        self.product1 = Product.objects.create(
            title="Apple",
            category="fruits",
            selling_price=Decimal("10.99"),
            discount_price=Decimal("1.99"),
            product_image="test_image.png",
        )
        self.product2 = Product.objects.create(
            title="Banana",
            category="fruits",
            selling_price=Decimal("10.99"),
            discount_price=Decimal("1.99"),
            product_image="test_image.png",
        )
        self.product3 = Product.objects.create(
            title="Orange",
            category="fruits",
            selling_price=Decimal("10.99"),
            discount_price=Decimal("1.99"),
            product_image="test_image.png",
        )

    def test_search_view_with_results(self):
        url = reverse("store_app:search")
        query = "Apple"
        response = self.client.get(url, {"search": query})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/search.html")
        self.assertContains(response, "Apple")
        self.assertContains(response, self.product1.title)

    def test_search_view_with_no_results(self):
        url = reverse("store_app:search")
        query = "Watermelon"
        response = self.client.get(url, {"search": query})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/search.html")
        self.assertContains(response, "")
        self.assertNotContains(response, "Apple")
        self.assertNotContains(response, "Banana")
        self.assertNotContains(response, "Orange")

    def test_search_view_with_empty_query(self):
        url = reverse("store_app:search")
        response = self.client.get(url, {"search": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/search.html")
        self.assertNotContains(response, "Search Results for")
        self.assertNotContains(response, "No results found")


class WishlistViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

        self.product1 = Product.objects.create(
            title="Product 1",
            category="fruits",
            selling_price=Decimal("10.99"),
            discount_price=Decimal("1.99"),
            product_image="test_image.png",
        )
        self.product2 = Product.objects.create(
            title="Product 2",
            category="fruits",
            selling_price=Decimal("10.99"),
            discount_price=Decimal("1.99"),
            product_image="test_image.png",
        )

    def test_show_wishlist_view(self):
        url = reverse("store_app:show-wishlist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/wishlist.html")

    def test_plus_wishlist_view(self):
        url = reverse("store_app:plus-wishlist")
        response = self.client.get(url, {"product_id": self.product1.pk})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Wishlist.objects.filter(user=self.user, product=self.product1).exists()
        )

    def test_minus_wishlist_view(self):
        wishlist_item = Wishlist.objects.create(user=self.user, product=self.product2)
        url = reverse("store_app:minus-wishlist")
        response = self.client.get(url, {"product_id": self.product2.pk})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Wishlist.objects.filter(user=self.user, product=self.product2).exists()
        )
