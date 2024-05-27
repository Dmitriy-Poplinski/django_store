from decimal import Decimal
import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .models import Product, Customer, Cart, Payment, OrderPlaced, Wishlist
from .forms import CustomerRegistrationForm, CustomerProfileForm
from payment.liqpay import LiqPay
from store_app.utils.utils import total_wishlist_items_util, change_amount_carts_util, change_cart_quantity_util


@login_required(login_url="login")
def home(request: HttpRequest) -> HttpResponse:
    total_item, wishlist_item = total_wishlist_items_util(request)

    return render(request, "app/home.html", locals())


@login_required(login_url="login")
def about(request: HttpRequest) -> HttpResponse:
    total_item, wishlist_item = total_wishlist_items_util(request)

    return render(request, "app/about.html", locals())


@login_required(login_url="login")
def contact(request: HttpRequest) -> HttpResponse:
    total_item, wishlist_item = total_wishlist_items_util(request)

    return render(request, "app/contact.html", locals())


class CategoryView(View, LoginRequiredMixin):
    @staticmethod
    def get(request: HttpRequest, name: str) -> HttpResponse:
        total_item, wishlist_item = total_wishlist_items_util(request)

        products = Product.objects.filter(category=name)
        titles = Product.objects.filter(category=name).values("title")

        return render(request, "app/category.html", locals())


class CategoryTitle(View, LoginRequiredMixin):
    @staticmethod
    def get(request: HttpRequest, name: str) -> HttpResponse:
        total_item, wishlist_item = total_wishlist_items_util(request)

        products = Product.objects.filter(title=name)
        titles = Product.objects.filter(category=products[0].category).values("title")

        return render(request, "app/category.html", locals())


class ProductDetail(View, LoginRequiredMixin):
    @staticmethod
    def get(request: HttpRequest, pk: int) -> HttpResponse:
        total_item, wishlist_item = total_wishlist_items_util(request)

        product = Product.objects.get(pk=pk)

        wishlist = Wishlist.objects.filter(product=product, user=request.user)

        return render(request, "app/product_detail.html", locals())


class CustomerRegistrationView(View):
    @staticmethod
    def get(request: HttpRequest) -> HttpResponse:
        total_item, wishlist_item = total_wishlist_items_util(request)

        form = CustomerRegistrationForm()

        return render(request, "app/customer_registration.html", locals())

    @staticmethod
    def post(request: HttpRequest) -> HttpResponse:
        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User registered successfully!")
        else:
            messages.warning(request, "Invalid input data, please try again.")

        return render(request, "app/customer_registration.html", locals())


class CustomerProfileView(View, LoginRequiredMixin):
    @staticmethod
    def get(request: HttpRequest) -> HttpResponse:
        total_item, wishlist_item = total_wishlist_items_util(request)

        form = CustomerProfileForm()

        return render(request, "app/profile.html", locals())

    @staticmethod
    def post(request: HttpRequest) -> HttpResponse:
        form = CustomerProfileForm(request.POST)

        if form.is_valid():
            user = request.user
            name = form.cleaned_data["name"]
            location = form.cleaned_data["location"]
            city = form.cleaned_data["city"]
            phone = form.cleaned_data["phone"]
            state = form.cleaned_data["state"]
            zip_code = form.cleaned_data["zip_code"]

            customer = Customer(
                user=user,
                name=name,
                location=location,
                city=city,
                phone=phone,
                state=state,
                zip_code=zip_code,
            )

            customer.save()

            messages.success(request, "Your profile has been saved successfully!")
        else:
            messages.warning(request, "Invalid input data, please try again.")

        return render(request, "app/profile.html", locals())


@login_required(login_url="login")
def address(request: HttpRequest) -> HttpResponse:
    total_item, wishlist_item = total_wishlist_items_util(request)

    addresses = Customer.objects.filter(user=request.user)

    return render(request, "app/address.html", locals())


class UpdateAddressView(View, LoginRequiredMixin):
    @staticmethod
    def get(request: HttpRequest, pk: int) -> HttpResponse:
        total_item, wishlist_item = total_wishlist_items_util(request)

        user_address = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=user_address)

        return render(request, "app/update_address.html", locals())

    @staticmethod
    def post(request: HttpRequest, pk: int) -> HttpResponse:
        form = CustomerProfileForm(request.POST)

        if form.is_valid():
            customer = Customer.objects.get(pk=pk)
            customer.name = form.cleaned_data["name"]
            customer.location = form.cleaned_data["location"]
            customer.city = form.cleaned_data["city"]
            customer.phone = form.cleaned_data["phone"]
            customer.state = form.cleaned_data["state"]
            customer.zip_code = form.cleaned_data["zip_code"]

            customer.save()

            messages.success(request, "Your profile has been updated successfully!")
        else:
            messages.warning(request, "Invalid input data, please try again.")

        return redirect("store_app:address")


class CheckoutView(View, LoginRequiredMixin):
    @staticmethod
    def get(request: HttpRequest) -> HttpResponse:
        total_item, wishlist_item = total_wishlist_items_util(request)

        user = request.user
        addresses = Customer.objects.filter(user=user)
        carts, total_amount = change_amount_carts_util(request)

        return render(request, "app/checkout.html", locals())

    @staticmethod
    def post(request: HttpRequest) -> HttpResponse:
        total_amount = str(Decimal(request.POST.get("total_amount", 0)))
        liqpay = LiqPay(
            public_key=settings.PUBLIC_LIQPAY_KEY,
            private_key=settings.PRIVATE_LIQPAY_KEY,
        )
        user = request.user

        order_id = str(uuid.uuid4())

        params = {
            "version": 3,
            "public_key": settings.PUBLIC_LIQPAY_KEY,
            "amount": total_amount,
            "currency": "USD",
            "description": f"Payment for order {order_id}",
            "order_id": order_id,
            "language": "en",
            "action": "pay",
            "result_url": "http://127.0.0.1:8000/store/payment-done/",
            "server_url": "http://127.0.0.1:8000/store/payment-done/",
        }

        response = liqpay.api(url="api/3/checkout", params=params)

        if response.status_code == 200:
            customer_id = request.POST.get("customer_id", None)
            customer = None

            if customer_id:
                customer = Customer.objects.get(pk=customer_id)
            else:
                messages.warning(request, "Please enter a valid address")

            payment_id = str(uuid.uuid4())

            payment = Payment(
                user=user,
                amount=total_amount,
                order_id=order_id,
                payment_status="pending",
                payment_id=payment_id,
            )
            payment.save()

            carts = Cart.objects.filter(user=user)

            for cart in carts:
                order_placed = OrderPlaced(
                    user=user,
                    customer=customer,
                    product=cart.product,
                    quantity=cart.quantity,
                    status="Pending",
                    payment=payment,
                )

                order_placed.save()

            messages.success(request, "Your order has been created successfully!")

        return redirect(response.url)


@login_required(login_url="login")
def add_to_cart(request: HttpRequest) -> HttpResponse:
    user = request.user
    product_id = request.GET.get("product_id", None)
    product = Product.objects.get(pk=product_id)

    Cart(user=user, product=product).save()

    return redirect("store_app:show-cart")


@login_required(login_url="login")
def show_cart(request: HttpRequest) -> HttpResponse:
    total_item, wishlist_item = total_wishlist_items_util(request)

    user = request.user
    carts, total_amount = change_amount_carts_util(request)

    return render(request, "app/add_to_cart.html", locals())


@login_required(login_url="login")
def show_wishlist(request: HttpRequest) -> HttpResponse:
    user = request.user

    total_item, wishlist_item = total_wishlist_items_util(request)

    products = Wishlist.objects.filter(user=user)

    return render(request, "app/wishlist.html", locals())


@login_required(login_url="login")
def plus_cart(request: HttpRequest) -> JsonResponse:
    cart = change_cart_quantity_util(request, 1)

    data = change_amount_carts_util(request, cart, "json")

    return JsonResponse(data, safe=False)


@login_required(login_url="login")
def minus_cart(request: HttpRequest) -> JsonResponse:
    cart = change_cart_quantity_util(request, -1)

    data = change_amount_carts_util(request, cart, "json")

    return JsonResponse(data)


@login_required(login_url="login")
def remove_cart(request: HttpRequest) -> JsonResponse:
    product_id = request.GET.get("product_id", None)
    cart = Cart.objects.get(Q(user=request.user) & Q(product=product_id))
    cart.delete()

    data = change_amount_carts_util(request, cart, "json")

    return JsonResponse(data)


@login_required(login_url="login")
def orders(request: HttpRequest) -> HttpResponse:
    total_item, wishlist_item = total_wishlist_items_util(request)

    order_placed = OrderPlaced.objects.filter(user=request.user)

    return render(request, "app/orders.html", locals())


@login_required(login_url="login")
def plus_wishlist(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        product_id = request.GET.get("product_id", None)
        product = Product.objects.get(pk=product_id)
        user = request.user
        Wishlist(user=user, product=product).save()

        data = {
            "message": "Added to Wishlist!",
        }

        return JsonResponse(data)


@login_required(login_url="login")
def minus_wishlist(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        product_id = request.GET.get("product_id", None)
        product = Product.objects.get(pk=product_id)
        user = request.user
        Wishlist.objects.filter(user=user, product=product).delete()

        data = {
            "message": "Remove from Wishlist!",
        }

        return JsonResponse(data)


@login_required(login_url="login")
def search(request: HttpRequest) -> HttpResponse:
    total_item, wishlist_item = total_wishlist_items_util(request)

    query = request.GET.get("search", None)
    products = Product.objects.filter(title__icontains=query)

    return render(request, "app/search.html", locals())
