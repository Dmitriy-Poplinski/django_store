from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("category/<slug:name>", views.CategoryView.as_view(), name="category"),
    path("category-title/<name>", views.CategoryTitle.as_view(), name="category-title"),
    path(
        "product-detail/<int:pk>", views.ProductDetail.as_view(), name="product-detail"
    ),
    path("profile/", views.CustomerProfileView.as_view(), name="profile"),
    path("address/", views.address, name="address"),
    path(
        "update-address/<int:pk>",
        views.UpdateAddressView.as_view(),
        name="update-address",
    ),
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),
    path("cart/", views.show_cart, name="show-cart"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("plus-cart/", views.plus_cart, name="plus-cart"),
    path("minus-cart/", views.minus_cart, name="minus-cart"),
    path("show-wishlist/", views.show_wishlist, name="show-wishlist"),
    path("plus-wishlist/", views.plus_wishlist, name="plus-wishlist"),
    path("minus-wishlist/", views.minus_wishlist, name="minus-wishlist"),
    path("remove-cart/", views.remove_cart, name="remove-cart"),
    path("orders/", views.orders, name="orders"),
    path("search/", views.search, name="search"),
    path(
        "password-reset-done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="app/password_reset_complete.html"
        ),
        name="password_reset_done",
    ),
]

app_name = "store_app"
