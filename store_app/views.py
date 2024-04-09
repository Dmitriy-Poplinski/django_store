from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import View
from django.contrib import messages

from .models import Product, Customer
from .forms import CustomerRegistrationForm, CustomerProfileForm


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "app/home.html")


def about(request: HttpRequest) -> HttpResponse:
    return render(request, "app/about.html")


def contact(request: HttpRequest) -> HttpResponse:
    return render(request, "app/contact.html")


class CategoryView(View):
    def get(self, request: HttpRequest, name: str) -> HttpResponse:
        products = Product.objects.filter(category=name)
        titles = Product.objects.filter(category=name).values("title")

        return render(request, "app/category.html", locals())


class CategoryTitle(View):
    def get(self, request: HttpRequest, name: str) -> HttpResponse:
        products = Product.objects.filter(title=name)
        titles = Product.objects.filter(category=products[0].category).values("title")

        return render(request, "app/category.html", locals())


class ProductDetail(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        product = Product.objects.get(pk=pk)

        return render(request, "app/product_detail.html", locals())


class CustomerRegistrationView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = CustomerRegistrationForm()

        return render(request, "app/customer_registration.html", locals())

    def post(self, request: HttpRequest) -> HttpResponse:
        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User registered successfully!")
        else:
            messages.warning(request, "Invalid input data, please try again.")

        return render(request, "app/customer_registration.html", locals())


class CustomerProfileView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = CustomerProfileForm()
        return render(request, "app/profile.html", locals())

    def post(self, request: HttpRequest) -> HttpResponse:
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


def address(request: HttpRequest) -> HttpResponse:
    addresses = Customer.objects.filter(user=request.user)

    return render(request, "app/address.html", locals())
