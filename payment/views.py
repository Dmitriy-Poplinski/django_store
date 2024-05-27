from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required

from store_app.utils.utils import total_wishlist_items_util


@login_required(login_url="login")
def payment_done(request: HttpRequest) -> HttpResponse:
    total_item, wishlist_item = total_wishlist_items_util(request)

    return render(request, "payment_done.html", locals())
