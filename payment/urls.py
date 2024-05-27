from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("payment-done/", views.payment_done, name="payment-done"),

]

app_name = "payments"
