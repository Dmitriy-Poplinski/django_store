from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

from store_app import forms
from store_app import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("store_app.urls")),
    path("", include("payment.urls")),
    path("register/", views.CustomerRegistrationView.as_view(), name="register"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="app/password_reset.html",
            form_class=forms.CustomerPasswordResetForm,
        ),
        name="password_reset",
    ),
    path(
        "password-reset-done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="app/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset/confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="app/password_reset_confirm.html",
            form_class=forms.CustomerPasswordSetForm,
            success_url="/store/password-reset-done/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="app/login.html", authentication_form=forms.CustomerLoginForm
        ),
        name="login",
    ),
    path(
        "password-change/",
        auth_views.PasswordChangeView.as_view(
            template_name="app/change_password.html",
            form_class=forms.CustomerPasswordChangeForm,
            success_url="/store/password-change-done/",
        ),
        name="password-change",
    ),
    path(
        "password-change-done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="app/password_change_done.html"
        ),
        name="password-change-done",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Django Store"
admin.site.site_title = "Django Store"
