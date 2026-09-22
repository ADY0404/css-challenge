from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    """
    Dedicated token generator for student email verification.
    Unlike standard password reset tokens which include user.last_login,
    this generator maintains validity across user login sessions while
    strictly invalidating once the email is verified, or if the email/password changes.
    """

    def _make_hash_value(self, user, timestamp):
        profile = getattr(user, 'profile', None)
        email_verified = profile.email_verified if profile else False
        email = user.email or ""
        return f"{user.pk}{user.password}{email}{email_verified}{timestamp}"


email_verification_token_generator = EmailVerificationTokenGenerator()

