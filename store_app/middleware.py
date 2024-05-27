from django.http import HttpResponseRedirect
from django.urls import reverse


class RedirectNotLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        login_url = reverse("login")
        register_url = reverse("register")

        if not request.user.is_authenticated and request.path not in [login_url, register_url]:
            return HttpResponseRedirect(login_url)

        response = self.get_response(request)
        return response
