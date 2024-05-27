from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib import admin
from django.urls import reverse

from .models import Payment
from .admin import PaymentAdmin
from .views import payment_done


class PaymentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.payment = Payment.objects.create(
            user=self.user,
            amount=100.0,
            order_id="ORD12345",
            payment_status="Completed",
            payment_id="PAY12345",
            paid=True,
        )

    def test_payment_creation(self):
        self.assertEqual(self.payment.user, self.user)
        self.assertEqual(self.payment.amount, 100.0)
        self.assertEqual(self.payment.order_id, "ORD12345")
        self.assertEqual(self.payment.payment_status, "Completed")
        self.assertEqual(self.payment.payment_id, "PAY12345")
        self.assertTrue(self.payment.paid)

    def test_payment_str_method(self):
        expected_str = f"{self.user.username}'s Payment 100.0 for ORD12345"
        self.assertEqual(str(self.payment), expected_str)

    def test_payment_default_values(self):
        new_payment = Payment.objects.create(
            user=self.user,
            amount=50.0,
        )
        self.assertIsNone(new_payment.order_id)
        self.assertIsNone(new_payment.payment_status)
        self.assertIsNone(new_payment.payment_id)
        self.assertFalse(new_payment.paid)


class PaymentAdminTest(TestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin", password="admin", email="admin@example.com"
        )
        self.user = User.objects.create_user(
            username="testuser", password="12345", email="testuser@example.com"
        )
        self.payment = Payment.objects.create(
            user=self.user,
            amount=100.0,
            order_id="ORD12345",
            payment_status="Completed",
            payment_id="PAY12345",
            paid=True,
        )
        self.client = Client()
        self.client.login(username="admin", password="admin")

    def test_payment_admin_registered(self):
        self.assertTrue(admin.site.is_registered(Payment))

    def test_payment_admin_list_display(self):
        payment_admin = PaymentAdmin(model=Payment, admin_site=admin.site)
        self.assertEqual(
            payment_admin.list_display,
            (
                "id",
                "user",
                "amount",
                "order_id",
                "payment_status",
                "payment_id",
                "paid",
            ),
        )


class PaymentDoneViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client = Client()

    def test_payment_done_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("payments:payment-done"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "payment_done.html")
