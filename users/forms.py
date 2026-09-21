from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    """Registration form matching the fields presented on the sign-up page."""

    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    year = forms.TypedChoiceField(
        choices=[("", "Year")] + [(str(year), f"Year {year}") for year in range(1, 11)],
        coerce=int,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "email", "username")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("You already have an account. kindly reset your password")
        return email


from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class UsernameOrEmailPasswordResetForm(PasswordResetForm):
    """
    Password reset form that allows users to supply either their account username
    or their registered email address.
    """
    username_or_email = forms.CharField(
        label="Username or Email",
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={
            "id": "id_username_or_email",
            "class": "form-control border-start-0",
            "placeholder": "student@example.edu",
            "autofocus": True,
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("email", None)
        # Gracefully handle POST requests that pass 'email' instead of 'username_or_email'
        if self.data and "email" in self.data and "username_or_email" not in self.data:
            data = self.data.copy()
            data["username_or_email"] = data["email"]
            self.data = data

    def clean_username_or_email(self):
        return self.cleaned_data["username_or_email"].strip()

    def get_users(self, lookup):
        """Given a username or email address, return matching active user(s) with a registered email."""
        UserModel = get_user_model()
        value = (lookup or "").strip()
        if not value:
            return []
        users = UserModel._default_manager.filter(
            Q(email__iexact=value) | Q(username__iexact=value),
            is_active=True,
        )
        email_field = UserModel.get_email_field_name()
        return (
            u for u in users
            if u.has_usable_password() and getattr(u, email_field, None)
        )

    def save(
        self,
        domain_override=None,
        subject_template_name="users/password_reset_subject.txt",
        email_template_name="users/password_reset_email.txt",
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
        html_email_template_name="users/password_reset_email.html",
        extra_email_context=None,
    ):
        """
        Generate a one-use link for resetting password and send it to the user.
        """
        UserModel = get_user_model()
        lookup = self.cleaned_data.get("username_or_email", "")
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override

        email_field_name = UserModel.get_email_field_name()
        for user in self.get_users(lookup):
            user_email = getattr(user, email_field_name)
            user_pk_bytes = force_bytes(UserModel._meta.pk.value_to_string(user))
            context = {
                "email": user_email,
                "domain": domain,
                "site_name": site_name,
                "uid": urlsafe_base64_encode(user_pk_bytes),
                "user": user,
                "token": token_generator.make_token(user),
                "protocol": "https" if use_https else "http",
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name,
                email_template_name,
                context,
                from_email,
                user_email,
                html_email_template_name=html_email_template_name,
            )

