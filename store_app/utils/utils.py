from django.http import HttpRequest
from django.db.models import Q

from store_app.models import Cart, Wishlist


def total_wishlist_items_util(request: HttpRequest) -> tuple:
    total_item = 0
    wishlist_item = 0

    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
        wishlist_item = len(Wishlist.objects.filter(user=request.user))

    return total_item, wishlist_item


def change_amount_carts_util(request: HttpRequest, cart: Cart = None, return_type: str = "req") -> dict | tuple:
    user = request.user
    carts = Cart.objects.filter(user=user)

    amount = 0

    for cart_item in carts:
        value = cart_item.product.price_with_discount * cart_item.quantity
        amount += value

    total_amount = amount + 4

    if return_type == "json":
        return {
            "quantity": cart.quantity,
            "total_amount": total_amount,
            "amount": amount,
        }
    elif return_type == "req":
        return carts, total_amount


def change_cart_quantity_util(request: HttpRequest, quantity: int) -> Cart:
    product_id = request.GET.get("product_id", None)
    cart = Cart.objects.get(Q(user=request.user) & Q(product=product_id))
    cart.quantity += quantity
    cart.save()

    return cart
