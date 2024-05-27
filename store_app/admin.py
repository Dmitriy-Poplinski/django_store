from django.contrib import admin
from .models import Product, Customer, Cart, Payment, OrderPlaced, Wishlist


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "discount_price", "category", "product_image")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "location", "city", "state", "zip_code")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "quantity")


@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "customer",
        "quantity",
        "ordered_date",
        "status",
        "payment",
    )


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "product",
    )
