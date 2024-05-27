from django.test import TestCase
from django.contrib.auth.models import User
from store_app.forms import (
    CustomerLoginForm,
    CustomerRegistrationForm,
    CustomerPasswordChangeForm,
    CustomerPasswordResetForm,
    CustomerPasswordSetForm,
    CustomerProfileForm,
)


class FormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser", password="1995testpassword1995"
        )

    def test_customer_login_form(self):
        form_data = {"username": "testuser", "password": "1995testpassword1995"}
        form = CustomerLoginForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")

    def test_customer_registration_form(self):
        form_data = {
            "username": "testuser2",
            "email": "test2@example.com",
            "password1": "1995testpassword21995",
            "password2": "1995testpassword21995",
        }
        form = CustomerRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")

    def test_customer_password_change_form(self):
        form_data = {
            "old_password": "1995testpassword1995",
            "new_password1": "1994testpassword31994",
            "new_password2": "1994testpassword31994",
        }
        form = CustomerPasswordChangeForm(user=self.user, data=form_data)
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")

    def test_customer_password_reset_form(self):
        form_data = {"email": "test1@example.com"}
        form = CustomerPasswordResetForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_customer_password_set_form(self):
        form_data = {
            "new_password1": "1994testpassword21994",
            "new_password2": "1994testpassword21994",
        }
        form = CustomerPasswordSetForm(user=self.user, data=form_data)
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")

    def test_customer_profile_form(self):
        form_data = {
            "name": "Test Name",
            "location": "Test Location",
            "city": "Test City",
            "phone": "1234567890",
            "state": "CA",
            "zip_code": "12345",
        }
        form = CustomerProfileForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")
