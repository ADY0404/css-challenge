from django.urls import path
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from .forms import UsernameOrEmailPasswordResetForm
from .views import (
    login_view,
    settings_view,
    signup_view,
    update_profile,
    member_profile,
    activate_account,
    resend_verification,
    email_verification_pending,
    CustomPasswordResetConfirmView,
)

urlpatterns = [
    # Obfuscated user URLs (masks internal route structure with hashed identifiers)
    path("u/p-8f2a7b/", update_profile, name="profile"),
    path("u/s-4d91ae/", settings_view, name="settings"),
    path("u/m-6c3e81/<str:username>/", member_profile, name="member_profile"),
    path("u/a-3e7b/<str:uidb64>/<str:token>/", activate_account, name="activate_account"),
    path("u/v-9c2a/", resend_verification, name="resend_verification"),
    path("u/v-pending/", email_verification_pending, name="email_verification_pending"),
    path(
        "u/r-5b2f9a/",
        auth_views.PasswordResetView.as_view(
            template_name="users/password_reset_form.html",
            form_class=UsernameOrEmailPasswordResetForm,
            email_template_name="users/password_reset_email.txt",
            html_email_template_name="users/password_reset_email.html",
            subject_template_name="users/password_reset_subject.txt",
        ),
        name="password_reset",
    ),
    path(
        "u/r-done-7e1b/",
        auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "u/r-cf-8a2b/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "u/r-ok-1f4e/",
        auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
        name="password_reset_complete",
    ),

    # Legacy & exploratory route redirects (masks internal structure)
    path("users/profile/", RedirectView.as_view(pattern_name="profile", permanent=False)),
    path("users/settings/", RedirectView.as_view(pattern_name="settings", permanent=False)),
    path("users/member/<str:username>/", RedirectView.as_view(pattern_name="member_profile", permanent=False)),
    path("users/password-reset/", RedirectView.as_view(pattern_name="password_reset", permanent=False)),
    path("profile/", RedirectView.as_view(pattern_name="profile", permanent=False)),
    path("settings/", RedirectView.as_view(pattern_name="settings", permanent=False)),
    path("member/<str:username>/", RedirectView.as_view(pattern_name="member_profile", permanent=False)),
]
