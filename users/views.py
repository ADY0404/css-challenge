import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.urls import reverse
from .forms import SignUpForm
from .models import Profile
from homepage.validators import validate_image_upload
from homepage.ratelimit import ratelimit, get_client_ip
from homepage.recaptcha import verify_recaptcha

logger = logging.getLogger(__name__)


def send_verification_email(request, user):
    """Generate a secure verification token and send a branded HTML confirmation email."""
    token = default_token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    activation_url = request.build_absolute_uri(
        reverse('activate_account', kwargs={'uidb64': uidb64, 'token': token})
    )
    display_name = user.first_name or user.username
    subject = "Confirm Ownership of Your Email Address - CSS Society"
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@localhost')

    # Plain-text fallback
    text_body = (
        f"Hi {display_name},\n\n"
        f"Thank you for joining the Computer Science Society!\n\n"
        f"Please confirm your email address by visiting this link:\n"
        f"{activation_url}\n\n"
        f"This link expires in 24 hours.\n"
        f"If you didn't create this account, you can safely ignore this email.\n\n"
        f"Best regards,\nComputer Science Society Team"
    )

    # HTML body — gradient header, button + fallback link, plain expiry, proper footer
    html_body = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>Confirm Your Email</title></head>
<body style="margin:0;padding:0;background:#f0f0f0;font-family:Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="padding:32px 16px;background:#f0f0f0;">
  <tr><td align="center">
    <table width="560" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:8px;overflow:hidden;max-width:560px;width:100%;">
      <!-- Gradient header -->
      <tr>
        <td style="background:linear-gradient(135deg,#1a1a2e 0%,#16213e 60%,#0f3460 100%);padding:32px 40px;text-align:center;">
          <h1 style="margin:0;color:#ffffff;font-size:20px;font-weight:700;">Computer Science Society</h1>
          <p style="margin:6px 0 0;color:#a0aec0;font-size:12px;">Email Verification</p>
        </td>
      </tr>
      <!-- Body -->
      <tr>
        <td style="padding:36px 40px 28px;">
          <p style="margin:0 0 16px;font-size:15px;color:#222222;line-height:1.6;">Hi {display_name},</p>
          <p style="margin:0 0 28px;font-size:15px;color:#444444;line-height:1.7;">
            Thanks for signing up. Click below to confirm your email and activate your account.
          </p>
          <table cellpadding="0" cellspacing="0">
            <tr>
              <td style="background:#0f3460;border-radius:6px;">
                <a href="{activation_url}" target="_blank"
                   style="display:inline-block;padding:12px 28px;color:#ffffff;font-size:14px;font-weight:bold;text-decoration:none;border-radius:6px;">
                  Confirm Email
                </a>
              </td>
            </tr>
          </table>
          <p style="margin:20px 0 0;font-size:13px;color:#888888;word-break:break-all;">
            Or copy this link into your browser:<br/>
            <a href="{activation_url}" style="color:#0f3460;font-size:12px;">{activation_url}</a>
          </p>
          <p style="margin:20px 0 0;font-size:13px;color:#888888;">
            This link expires in 24 hours. If you didn't sign up, just ignore this.
          </p>
        </td>
      </tr>
      <!-- Footer -->
      <tr>
        <td style="background:#f7fafc;border-top:1px solid #e2e8f0;padding:20px 40px;text-align:center;">
          <p style="margin:0 0 4px;color:#718096;font-size:12px;">
            This email was sent to <strong>{user.email}</strong>
          </p>
          <p style="margin:0;color:#a0aec0;font-size:11px;">
            &copy; Computer Science Society &nbsp;&middot;&nbsp; All rights reserved
          </p>
        </td>
      </tr>
    </table>
  </td></tr>
</table>
</body></html>"""

    logger.info("Dispatching email verification to '%s' (user: %s).", user.email, user.username)
    try:
        msg = EmailMultiAlternatives(subject, text_body, from_email, [user.email])
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=False)
        logger.info("Verification email sent to '%s'.", user.email)
    except Exception as exc:
        logger.error("Failed to send verification email to '%s': %s", user.email, exc)


@ratelimit(rate='5/m', action='login')
def login_view(request):
    """Handle user authentication, 5-strike account lockout, and 10-minute cooldown enforcement."""
    if request.user.is_authenticated:
        return redirect("home")

    context = {}

    if request.method == "POST":
        # 1. reCAPTCHA verification
        recaptcha_token = request.POST.get('g-recaptcha-response', '').strip()
        client_ip = get_client_ip(request)
        is_recaptcha_valid, recaptcha_err = verify_recaptcha(recaptcha_token, remote_ip=client_ip)
        if not is_recaptcha_valid:
            logger.warning("reCAPTCHA failed on login from IP %s", client_ip)
            messages.error(request, recaptcha_err)
            return render(request, "users/login.html", context)

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        # Check if account exists by username or email
        user_match = User.objects.filter(username__iexact=username).first()
        if not user_match:
            user_match = User.objects.filter(email__iexact=username).first()

        # 2. Check if account is deactivated, locked or in cooldown
        if user_match:
            if not user_match.is_active:
                logger.warning("Blocked login attempt for deactivated user '%s'.", user_match.username)
                messages.error(request, "This account has been deactivated. Please contact society administration to reactivate your account.")
                return render(request, "users/login.html", context)

            profile, _ = Profile.objects.get_or_create(user=user_match)
            is_locked, lock_reason, remaining_mins = profile.get_lock_status()
            if is_locked:
                logger.warning("Blocked login attempt for locked account '%s'. Reason: %s", user_match.username, lock_reason)
                messages.error(request, lock_reason)
                context["is_locked"] = True
                context["remaining_mins"] = remaining_mins
                return render(request, "users/login.html", context)

        # 3. Authenticate
        user = authenticate(request, username=username, password=password)
        if user is None and user_match:
            user = authenticate(request, username=user_match.username, password=password)

        if user is not None:
            profile, _ = Profile.objects.get_or_create(user=user)

            # 4. Check email verification (admin / staff / superuser exempt)
            is_admin = user.is_staff or user.is_superuser
            require_verification = True
            try:
                from homepage.models import SiteConfiguration
                site_config = SiteConfiguration.get_solo()
                if site_config:
                    require_verification = site_config.require_email_verification
            except Exception:
                pass

            if not is_admin and require_verification and not profile.email_verified:
                logger.warning("Blocked login attempt for unverified user '%s'.", user.username)
                messages.error(
                    request,
                    "Your email address is not verified. Please check your inbox and verify your email before logging in."
                )
                context["unverified_account"] = True
                context["unverified_email"] = user.email
                return render(request, "users/login.html", context)

            profile.register_successful_login()
            login(request, user)
            logger.info("User '%s' logged in successfully.", user.username)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next')
            return redirect(next_url if next_url else "home")
        else:
            max_attempts = 5
            try:
                from homepage.models import SiteConfiguration
                site_config = SiteConfiguration.get_solo()
                if site_config:
                    max_attempts = site_config.max_login_attempts
            except Exception:
                pass

            if user_match:
                profile, _ = Profile.objects.get_or_create(user=user_match)
                profile.register_failed_login(max_attempts=max_attempts)
                if profile.is_locked:
                    logger.warning("Account '%s' locked after %d failed login attempts.", user_match.username, max_attempts)
                    messages.error(
                        request,
                        f"Your account is locked due to {max_attempts} incorrect login attempts. Kindly reset your password to regain access."
                    )
                    context["is_locked"] = True
                else:
                    remaining = max_attempts - profile.failed_login_attempts
                    logger.info("Failed login for user '%s'. %d attempts remaining.", user_match.username, remaining)
                    messages.error(
                        request,
                        f"Invalid username or password. You have {remaining} attempt(s) remaining before account lockout."
                    )
            else:
                logger.info("Failed login attempt for nonexistent user '%s'.", username)
                messages.error(request, "Invalid username or password. Please try again.")

    return render(request, "users/login.html", context)


@ratelimit(rate='3/h', action='signup')
def signup_view(request):
    """Handle new user registration with profile creation and token-based email ownership confirmation."""
    if request.user.is_authenticated:
        return redirect("home")

    try:
        from homepage.models import SiteConfiguration
        site_config = SiteConfiguration.get_solo()
        if site_config and not site_config.allow_user_registration:
            messages.warning(request, "Student registration is currently closed by the platform administrator.")
            return redirect("login")
    except Exception:
        pass

    if request.method == "POST":
        # 1. reCAPTCHA verification
        recaptcha_token = request.POST.get('g-recaptcha-response', '').strip()
        client_ip = get_client_ip(request)
        is_recaptcha_valid, recaptcha_err = verify_recaptcha(recaptcha_token, remote_ip=client_ip)
        if not is_recaptcha_valid:
            logger.warning("reCAPTCHA failed on signup from IP %s", client_ip)
            messages.error(request, recaptcha_err)
            form = SignUpForm(request.POST)
            return render(request, "users/signup.html", {"form": form})

        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.year = form.cleaned_data.get("year")
            profile.email_verified = False
            profile.save()

            # Dispatch ownership confirmation email
            send_verification_email(request, user)

            login(request, user)
            logger.info("New user '%s' signed up successfully. Verification email dispatched.", user.username)
            messages.success(request, "Your account has been created. A verification link has been sent to confirm email ownership!")
            return redirect("home")
        else:
            # Form validation errors are displayed inline with each form field inside signup.html
            pass
    else:
        form = SignUpForm()
    return render(request, "users/signup.html", {"form": form})


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """
    Password reset confirmation view:
    Resets credentials, puts account in 10-minute cooldown, and prevents immediate login.
    """
    template_name = "users/password_reset_confirm.html"

    def form_valid(self, form):
        user = form.save()
        profile, _ = Profile.objects.get_or_create(user=user)
        cooldown_mins = 10
        try:
            from homepage.models import SiteConfiguration
            site_config = SiteConfiguration.get_solo()
            if site_config:
                cooldown_mins = site_config.lockout_duration_minutes
        except Exception:
            pass

        # Put account in security cooldown (default 10 mins)
        profile.schedule_post_reset_cooldown(minutes=cooldown_mins)
        logger.info("Password reset completed for '%s'. Account in %d-minute cooldown.", user.username, cooldown_mins)
        messages.success(
            self.request,
            f"Your password has been reset successfully! For your security, your account will open in {cooldown_mins} minutes. You cannot log in immediately."
        )
        return redirect("password_reset_complete")




def activate_account(request, uidb64, token):
    """Activate user account / mark email verified after token validation."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.email_verified = True
        profile.save()
        messages.success(request, "Your email has been verified successfully! Welcome to CSS.")
        if not request.user.is_authenticated:
            login(request, user)
        return redirect("home")
    else:
        messages.error(request, "The activation link is invalid or has expired.")
        return redirect("login")


@ratelimit(rate='3/h', action='resend_verification')
def resend_verification(request):
    """Resend account verification email for authenticated users or unverified users requesting via email."""
    if request.user.is_authenticated:
        profile, _ = Profile.objects.get_or_create(user=request.user)
        if profile.email_verified:
            messages.info(request, "Your email address is already verified.")
        else:
            send_verification_email(request, request.user)
            messages.success(request, f"A new verification link has been sent to {request.user.email}.")
        return redirect(request.META.get('HTTP_REFERER') or 'profile')

    # Unauthenticated user requesting a verification link
    email = (request.POST.get('email', '') or request.GET.get('email', '')).strip()
    if email:
        try:
            target_user = User.objects.filter(email__iexact=email).first()
            if target_user:
                target_profile, _ = Profile.objects.get_or_create(user=target_user)
                if target_profile.email_verified:
                    messages.info(request, "Your email address is already verified. You can log in directly.")
                else:
                    send_verification_email(request, target_user)
                    messages.success(request, f"A new verification link has been sent to {target_user.email}.")
            else:
                messages.info(request, "If an account exists with that email address, a verification link has been sent.")
        except Exception as e:
            logger.exception("Error resending verification email: %s", e)
            messages.error(request, "Unable to send verification email. Please try again later.")
    else:
        messages.warning(request, "Please provide your email address to receive a verification link.")

    return redirect("login")



@login_required
def update_profile(request):
    """Update member personal details, avatar, bio, and credentials."""
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            is_valid, error_msg = validate_image_upload(
                profile_picture,
                max_size_mb=2,
                min_width=100,
                min_height=100,
                max_width=2000,
                max_height=2000,
                target_aspect_ratio=1.0,
                aspect_ratio_tolerance=0.25,
                allowed_formats=('JPEG', 'PNG', 'WEBP')
            )
            if not is_valid:
                messages.error(request, error_msg)
                return redirect('profile')
            profile.profile_picture = profile_picture

        user.first_name = request.POST.get('first_name', user.first_name).strip()
        user.last_name = request.POST.get('last_name', user.last_name).strip()

        year = request.POST.get('year')
        if year:
            try:
                profile.year = int(year)
            except (ValueError, TypeError):
                pass

        profile.department = request.POST.get('department', profile.department).strip()
        profile.bio = request.POST.get('bio', profile.bio).strip()
        profile.github_url = request.POST.get('github_url', profile.github_url or '').strip() or None
        profile.linkedin_url = request.POST.get('linkedin_url', profile.linkedin_url or '').strip() or None

        old_password = request.POST.get('old_password', '').strip()
        password = request.POST.get('password', '').strip()
        password_changed = False
        if password:
            if not old_password:
                messages.error(request, "Current password is required to set a new password.")
                return redirect('profile')
            if not user.check_password(old_password):
                messages.error(request, "Incorrect current password. Password change aborted.")
                return redirect('profile')
            if len(password) < 6:
                messages.error(request, "New password must be at least 6 characters long.")
                return redirect('profile')
            user.set_password(password)
            password_changed = True

        user.save()
        profile.save()

        if password_changed:
            update_session_auth_hash(request, user)

        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('profile')

    return render(request, 'users/profile.html')


@login_required
def settings_view(request):
    """Manage notification, privacy, and account preferences."""
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'notifications':
            profile.email_digest = 'email_digest' in request.POST
            profile.challenge_notifications = 'challenge_notifications' in request.POST
            profile.internship_notifications = 'internship_notifications' in request.POST
            profile.community_mentions = 'community_mentions' in request.POST
            profile.save()
            messages.success(request, 'Your notification preferences have been saved.')
        elif action == 'privacy':
            profile.show_on_leaderboard = 'show_on_leaderboard' in request.POST
            profile.public_profile = 'public_profile' in request.POST
            profile.save()
            messages.success(request, 'Your community privacy settings have been updated.')
        elif action == 'deactivate':
            confirm_password = request.POST.get('confirm_password', '')
            if not user.check_password(confirm_password):
                messages.error(request, 'Incorrect password. Account deactivation cancelled.')
                return redirect('settings')
            user.is_active = False
            user.save()
            from django.contrib.auth import logout
            logout(request)
            logger.info("User '%s' deactivated their account.", user.username)
            messages.info(request, 'Your account has been deactivated. If you wish to reactivate in the future, please contact society administration.')
            return redirect('home')
        return redirect('settings')

    return render(request, 'users/settings.html')


def member_profile(request, username):
    """View another member's public society profile, bio, links, and challenge portfolio."""
    member_user = get_object_or_404(User, username=username)
    member_profile, _ = Profile.objects.get_or_create(user=member_user)

    is_self = request.user.is_authenticated and request.user.id == member_user.id
    can_view = member_profile.public_profile or is_self or (request.user.is_authenticated and request.user.is_staff)

    if not can_view:
        return render(request, "users/private_profile.html", {"member_user": member_user, "is_self": is_self})

    submissions = member_user.challenge_submissions.select_related('challenge').order_by('-submitted_at')
    messages_count = member_user.community_messages.count()
    from homepage.models import get_user_badges
    badges = get_user_badges(member_user)

    context = {
        "member_user": member_user,
        "member_profile": member_profile,
        "submissions": submissions,
        "submissions_count": submissions.count(),
        "messages_count": messages_count,
        "badges": badges,
        "is_self": is_self,
    }
    return render(request, "users/member_profile.html", context)

