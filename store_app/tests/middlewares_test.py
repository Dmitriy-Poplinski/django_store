from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.http import HttpResponseRedirect
from store_app.middleware import RedirectNotLoginMiddleware


class RedirectNotLoginMiddlewareTest(TestCase):
    def setUp(self):
        self.middleware = RedirectNotLoginMiddleware(get_response=lambda x: None)
        self.factory = RequestFactory()
        self.login_url = reverse("login")
        self.register_url = reverse("register")

    def test_redirect_authenticated_user_to_login_page(self):
        request = self.factory.get("/")
        request.user = AnonymousUser()

        response = self.middleware(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, self.login_url)

    def test_allow_authenticated_user_to_access_login_page(self):
        request = self.factory.get(self.login_url)
        request.user = AnonymousUser()

        response = self.middleware(request)

        self.assertIsNone(response)

    def test_allow_authenticated_user_to_access_register_page(self):
        request = self.factory.get(self.register_url)
        request.user = AnonymousUser()

        response = self.middleware(request)

        self.assertIsNone(response)

    def test_allow_authenticated_user_to_access_other_pages(self):
        request = self.factory.get("/some-other-page/")
        request.user = AnonymousUser()

        response = self.middleware(request)

        self.assertIsNotNone(response)

    def test_allow_unauthenticated_user_to_access_login_page(self):
        request = self.factory.get(self.login_url)
        request.user = AnonymousUser()

        response = self.middleware(request)

        self.assertIsNone(response)

    def test_allow_unauthenticated_user_to_access_register_page(self):
        request = self.factory.get(self.register_url)
        request.user = AnonymousUser()

        response = self.middleware(request)

        self.assertIsNone(response)

    def test_redirect_unauthenticated_user_from_other_pages_to_login_page(self):
        request = self.factory.get("/some-other-page/")
        request.user = AnonymousUser()

        response = self.middleware(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, self.login_url)
