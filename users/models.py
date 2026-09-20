from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    department = models.CharField(max_length=120, blank=True, default='Computer Science')
    bio = models.TextField(blank=True, default='')
    github_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)

    # Verification status
    email_verified = models.BooleanField(default=False)

    # Account lockout & cooldown security fields
    failed_login_attempts = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=False)
    locked_at = models.DateTimeField(null=True, blank=True)
    password_reset_at = models.DateTimeField(null=True, blank=True)
    unlock_at = models.DateTimeField(null=True, blank=True)

    # Notification preferences
    email_digest = models.BooleanField(default=True)
    challenge_notifications = models.BooleanField(default=True)
    internship_notifications = models.BooleanField(default=True)
    community_mentions = models.BooleanField(default=False)

    # Privacy preferences
    show_on_leaderboard = models.BooleanField(default=True)
    public_profile = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

    def register_failed_login(self, max_attempts=5):
        """Record an incorrect login attempt; lock if threshold reached."""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= max_attempts:
            self.is_locked = True
            from django.utils import timezone
            self.locked_at = timezone.now()
        self.save()

    def register_successful_login(self):
        """Reset failed attempt counters upon successful authentication."""
        if self.failed_login_attempts > 0 or self.is_locked:
            self.failed_login_attempts = 0
            self.is_locked = False
            self.locked_at = None
            self.unlock_at = None
            self.save()

    def schedule_post_reset_cooldown(self, minutes=10):
        """Place account in temporary cooldown after password reset (must not login right away)."""
        import datetime
        from django.utils import timezone
        now = timezone.now()
        self.password_reset_at = now
        self.unlock_at = now + datetime.timedelta(minutes=minutes)
        self.is_locked = True
        self.failed_login_attempts = 0
        self.save()

    def get_lock_status(self):
        """
        Check if account is currently locked or in cooldown.
        Returns:
            tuple (is_locked: bool, reason: str or None, remaining_minutes: int or None)
        """
        if not self.is_locked:
            return False, None, None

        from django.utils import timezone
        import math
        now = timezone.now()

        # If locked with a scheduled unlock time (post-reset cooldown)
        if self.unlock_at:
            if now >= self.unlock_at:
                # Cooldown has expired! Auto-unlock
                self.is_locked = False
                self.failed_login_attempts = 0
                self.locked_at = None
                self.unlock_at = None
                self.save()
                return False, None, None
            else:
                remaining_secs = (self.unlock_at - now).total_seconds()
                remaining_mins = max(1, math.ceil(remaining_secs / 60))
                return (
                    True,
                    f"Your account is locked following a password reset. For security, your account will open in {remaining_mins} minute(s). Please try again shortly.",
                    remaining_mins,
                )

        # Locked due to 5 failed attempts without password reset completed
        return (
            True,
            "Your account is locked due to 5 incorrect login attempts. Kindly reset your password to regain access.",
            None,
        )



@receiver(pre_save, sender=User)
def validate_user_email_unique(sender, instance, **kwargs):
    """Normalize user email and enforce case-insensitive uniqueness before saving."""
    if instance.email:
        normalized = instance.email.strip().lower()
        instance.email = normalized
        qs = User.objects.filter(email__iexact=normalized)
        if instance.pk:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise ValidationError({'email': 'A user with this email address already exists.'})