from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    login_view,
    settings_view,
    signup_view,
    update_profile,
    member_profile,
    activate_account,
    resend_verification,
    CustomPasswordResetConfirmView,
)

urlpatterns = [
    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("activate/<str:uidb64>/<str:token>/", activate_account, name="activate_account"),
    path("resend-verification/", resend_verification, name="resend_verification"),
    path("profile/", update_profile, name="profile"),
    path("member/<str:username>/", member_profile, name="member_profile"),
    path("settings/", settings_view, name="settings"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(template_name="users/password_reset_form.html"),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
        name="password_reset_complete",
    ),
]
