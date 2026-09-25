from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.urls import path, reverse
from django.utils import timezone
from django.utils.html import format_html
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Student Profile, Security & Preferences'
    fk_name = 'user'
    readonly_fields = ('account_status_banner',)
    fieldsets = (
        ('Account Status & Quick Actions', {
            'fields': ('account_status_banner',),
        }),
        ('Academic & Bio', {
            'fields': ('department', 'year', 'bio', 'profile_picture')
        }),
        ('Security & Verification', {
            'fields': ('email_verified', 'is_locked', 'failed_login_attempts', 'locked_at', 'unlock_at')
        }),
        ('Social & Portfolio', {
            'fields': ('github_url', 'linkedin_url')
        }),
        ('Notification Preferences', {
            'fields': ('email_digest', 'challenge_notifications', 'internship_notifications', 'community_mentions')
        }),
        ('Privacy Settings', {
            'fields': ('show_on_leaderboard', 'public_profile')
        }),
    )

    @admin.display(description='Account Status')
    def account_status_banner(self, instance):
        if not instance.user_id:
            return '-'
        user = instance.user
        if not user.is_active:
            reactivate_url = reverse('admin:user_reactivate', args=[user.pk])
            return format_html(
                '<div style="background:#fff3cd; border:1px solid #ffeeba; color:#856404; padding:10px 14px; border-radius:6px; margin:4px 0 10px 0;">'
                '<strong>⚠️ This account is currently DEACTIVATED.</strong> The student cannot log in.<br>'
                '<a class="button" style="background:#198754; color:white; padding:5px 16px; border-radius:4px; text-decoration:none; font-weight:bold; margin-top:8px; display:inline-block;" href="{}">✓ Reactivate Account Now</a>'
                '</div>',
                reactivate_url
            )
        elif instance.is_locked:
            unlock_url = reverse('admin:user_unlock', args=[user.pk])
            return format_html(
                '<div style="background:#f8d7da; border:1px solid #f5c6cb; color:#721c24; padding:10px 14px; border-radius:6px; margin:4px 0 10px 0;">'
                '<strong>🔒 This account is LOCKED</strong> due to incorrect password attempts or security cooldown.<br>'
                '<a class="button" style="background:#fd7e14; color:white; padding:5px 16px; border-radius:4px; text-decoration:none; font-weight:bold; margin-top:8px; display:inline-block;" href="{}">🔓 Unlock Account Now</a>'
                '</div>',
                unlock_url
            )
        else:
            deactivate_url = reverse('admin:user_deactivate', args=[user.pk])
            return format_html(
                '<div style="background:#d1e7dd; border:1px solid #badbcc; color:#0f5132; padding:10px 14px; border-radius:6px; margin:4px 0 10px 0;">'
                '<strong>🟢 Account is ACTIVE.</strong> The user can freely log in and participate.<br>'
                '<a class="button" style="background:#dc3545; color:white; padding:4px 12px; border-radius:4px; text-decoration:none; margin-top:8px; display:inline-block; font-size:12px;" href="{}">Deactivate Account</a>'
                '</div>',
                deactivate_url
            )


class CustomUserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'get_department',
        'get_year',
        'account_status_badge',
        'is_staff',
        'quick_actions',
    )
    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
        'profile__is_locked',
        'profile__email_verified',
        'profile__department',
    )
    list_select_related = ('profile',)
    actions = [
        'activate_selected_users',
        'deactivate_selected_users',
        'unlock_selected_users',
        'lock_selected_users',
        'verify_selected_emails',
    ]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:user_id>/reactivate/', self.admin_site.admin_view(self.reactivate_user_view), name='user_reactivate'),
            path('<int:user_id>/deactivate/', self.admin_site.admin_view(self.deactivate_user_view), name='user_deactivate'),
            path('<int:user_id>/unlock/', self.admin_site.admin_view(self.unlock_user_view), name='user_unlock'),
        ]
        return custom_urls + urls

    def reactivate_user_view(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        user.is_active = True
        user.save()
        if hasattr(user, 'profile'):
            user.profile.is_locked = False
            user.profile.failed_login_attempts = 0
            user.profile.locked_at = None
            user.profile.unlock_at = None
            user.profile.save()
        messages.success(request, f"User account '@{user.username}' has been successfully reactivated and unlocked.")
        return redirect(request.META.get('HTTP_REFERER') or 'admin:auth_user_changelist')

    def deactivate_user_view(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        user.is_active = False
        user.save()
        messages.warning(request, f"User account '@{user.username}' has been deactivated.")
        return redirect(request.META.get('HTTP_REFERER') or 'admin:auth_user_changelist')

    def unlock_user_view(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        user.is_active = True
        user.save()
        if hasattr(user, 'profile'):
            user.profile.is_locked = False
            user.profile.failed_login_attempts = 0
            user.profile.locked_at = None
            user.profile.unlock_at = None
            user.profile.save()
        messages.success(request, f"User account '@{user.username}' has been unlocked and reactivated.")
        return redirect(request.META.get('HTTP_REFERER') or 'admin:auth_user_changelist')

    @admin.display(description='Department')
    def get_department(self, instance):
        if hasattr(instance, 'profile'):
            return instance.profile.department
        return '-'

    @admin.display(description='Year')
    def get_year(self, instance):
        if hasattr(instance, 'profile') and instance.profile.year:
            return instance.profile.year_display
        return '-'

    @admin.display(description='Account Status')
    def account_status_badge(self, instance):
        is_locked = hasattr(instance, 'profile') and instance.profile.is_locked
        if not instance.is_active:
            return format_html('<span style="color:#721c24; font-weight:bold; background:#f8d7da; padding:3px 8px; border-radius:4px; border:1px solid #f5c6cb;">🔴 Deactivated</span>')
        elif is_locked:
            return format_html('<span style="color:#856404; font-weight:bold; background:#fff3cd; padding:3px 8px; border-radius:4px; border:1px solid #ffeeba;">🔒 Locked</span>')
        elif hasattr(instance, 'profile') and not instance.profile.email_verified:
            return format_html('<span style="color:#495057; background:#e9ecef; padding:3px 8px; border-radius:4px; border:1px solid #ced4da;">✉️ Unverified</span>')
        return format_html('<span style="color:#0f5132; font-weight:bold; background:#d1e7dd; padding:3px 8px; border-radius:4px; border:1px solid #badbcc;">🟢 Active</span>')

    @admin.display(description='Actions')
    def quick_actions(self, instance):
        is_locked = hasattr(instance, 'profile') and instance.profile.is_locked
        if not instance.is_active:
            reactivate_url = reverse('admin:user_reactivate', args=[instance.pk])
            return format_html(
                '<a class="button" style="background:#198754; color:white; padding:3px 10px; border-radius:4px; text-decoration:none; font-weight:bold; font-size:12px; display:inline-block;" href="{}">Reactivate</a>',
                reactivate_url
            )
        buttons = []
        if is_locked:
            unlock_url = reverse('admin:user_unlock', args=[instance.pk])
            buttons.append(format_html(
                '<a class="button" style="background:#fd7e14; color:white; padding:3px 8px; border-radius:4px; text-decoration:none; font-size:12px;" href="{}">Unlock</a>',
                unlock_url
            ))
        deactivate_url = reverse('admin:user_deactivate', args=[instance.pk])
        buttons.append(format_html(
            '<a class="button" style="background:#dc3545; color:white; padding:3px 8px; border-radius:4px; text-decoration:none; font-size:12px;" href="{}">Deactivate</a>',
            deactivate_url
        ))
        return format_html('&nbsp;'.join(buttons))

    @admin.action(description='Reactivate selected user accounts (set active and unlock)')
    def activate_selected_users(self, request, queryset):
        user_ids = list(queryset.values_list('id', flat=True))
        User.objects.filter(id__in=user_ids).update(is_active=True)
        Profile.objects.filter(user_id__in=user_ids).update(
            is_locked=False,
            failed_login_attempts=0,
            locked_at=None,
            unlock_at=None
        )
        if request:
            self.message_user(request, f"Successfully reactivated and unlocked {len(user_ids)} user accounts.")

    @admin.action(description='Deactivate selected user accounts')
    def deactivate_selected_users(self, request, queryset):
        count = queryset.update(is_active=False)
        if request:
            self.message_user(request, f"Successfully deactivated {count} user accounts.")

    @admin.action(description='Unlock selected user accounts (clear cooldown & reactivate)')
    def unlock_selected_users(self, request, queryset):
        user_ids = list(queryset.values_list('id', flat=True))
        User.objects.filter(id__in=user_ids).update(is_active=True)
        Profile.objects.filter(user_id__in=user_ids).update(
            is_locked=False,
            failed_login_attempts=0,
            locked_at=None,
            unlock_at=None
        )
        if request:
            self.message_user(request, f"Successfully unlocked and reactivated {len(user_ids)} user accounts.")

    @admin.action(description='Lock selected user accounts')
    def lock_selected_users(self, request, queryset):
        user_ids = list(queryset.values_list('id', flat=True))
        Profile.objects.filter(user_id__in=user_ids).update(is_locked=True, locked_at=timezone.now())
        if request:
            self.message_user(request, f"Successfully locked {len(user_ids)} user accounts.")

    @admin.action(description='Mark selected users as email verified')
    def verify_selected_emails(self, request, queryset):
        user_ids = list(queryset.values_list('id', flat=True))
        Profile.objects.filter(user_id__in=user_ids).update(email_verified=True)
        if request:
            self.message_user(request, f"Marked {len(user_ids)} users as email verified.")


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'get_email',
        'department',
        'year',
        'account_status_badge',
        'email_verified',
        'quick_actions',
    )
    list_filter = (
        'user__is_active',
        'is_locked',
        'email_verified',
        'department',
        'year',
        'show_on_leaderboard',
        'public_profile',
    )
    search_fields = (
        'user__username',
        'user__email',
        'user__first_name',
        'user__last_name',
        'department',
        'bio',
    )
    list_select_related = ('user',)
    actions = [
        'activate_profiles',
        'deactivate_profiles',
        'unlock_accounts',
        'lock_accounts',
        'verify_emails',
        'unverify_emails',
        'reset_failed_attempts'
    ]
    readonly_fields = ('account_status_banner',)
    fieldsets = (
        ('Account Status & Quick Actions', {
            'fields': ('account_status_banner',),
        }),
        ('Member Identification', {
            'fields': ('user', 'profile_picture')
        }),
        ('Security & Account Access Control', {
            'fields': ('email_verified', 'is_locked', 'failed_login_attempts', 'locked_at', 'unlock_at'),
            'description': 'Admin controls to lock/unlock accounts, verify emails, or reset cooldowns.'
        }),
        ('Academic Details', {
            'fields': ('department', 'year', 'bio')
        }),
        ('Links', {
            'fields': ('github_url', 'linkedin_url')
        }),
        ('Notification Preferences', {
            'fields': ('email_digest', 'challenge_notifications', 'internship_notifications', 'community_mentions')
        }),
        ('Privacy', {
            'fields': ('show_on_leaderboard', 'public_profile')
        }),
    )

    @admin.display(description='Email')
    def get_email(self, instance):
        return instance.user.email if instance.user else '-'

    @admin.display(description='Account Status')
    def account_status_badge(self, instance):
        if not instance.user or not instance.user.is_active:
            return format_html('<span style="color:#721c24; font-weight:bold; background:#f8d7da; padding:3px 8px; border-radius:4px; border:1px solid #f5c6cb;">🔴 Deactivated</span>')
        elif instance.is_locked:
            return format_html('<span style="color:#856404; font-weight:bold; background:#fff3cd; padding:3px 8px; border-radius:4px; border:1px solid #ffeeba;">🔒 Locked</span>')
        elif not instance.email_verified:
            return format_html('<span style="color:#495057; background:#e9ecef; padding:3px 8px; border-radius:4px; border:1px solid #ced4da;">✉️ Unverified</span>')
        return format_html('<span style="color:#0f5132; font-weight:bold; background:#d1e7dd; padding:3px 8px; border-radius:4px; border:1px solid #badbcc;">🟢 Active</span>')

    @admin.display(description='Actions')
    def quick_actions(self, instance):
        if not instance.user:
            return '-'
        if not instance.user.is_active:
            reactivate_url = reverse('admin:user_reactivate', args=[instance.user.pk])
            return format_html(
                '<a class="button" style="background:#198754; color:white; padding:3px 10px; border-radius:4px; text-decoration:none; font-weight:bold; font-size:12px; display:inline-block;" href="{}">Reactivate</a>',
                reactivate_url
            )
        buttons = []
        if instance.is_locked:
            unlock_url = reverse('admin:user_unlock', args=[instance.user.pk])
            buttons.append(format_html(
                '<a class="button" style="background:#fd7e14; color:white; padding:3px 8px; border-radius:4px; text-decoration:none; font-size:12px;" href="{}">Unlock</a>',
                unlock_url
            ))
        deactivate_url = reverse('admin:user_deactivate', args=[instance.user.pk])
        buttons.append(format_html(
            '<a class="button" style="background:#dc3545; color:white; padding:3px 8px; border-radius:4px; text-decoration:none; font-size:12px;" href="{}">Deactivate</a>',
            deactivate_url
        ))
        return format_html('&nbsp;'.join(buttons))

    @admin.display(description='Account Status')
    def account_status_banner(self, instance):
        if not instance.user or not instance.user_id:
            return '-'
        user = instance.user
        if not user.is_active:
            reactivate_url = reverse('admin:user_reactivate', args=[user.pk])
            return format_html(
                '<div style="background:#fff3cd; border:1px solid #ffeeba; color:#856404; padding:10px 14px; border-radius:6px; margin:4px 0 10px 0;">'
                '<strong>⚠️ This account is currently DEACTIVATED.</strong> The student cannot log in.<br>'
                '<a class="button" style="background:#198754; color:white; padding:5px 16px; border-radius:4px; text-decoration:none; font-weight:bold; margin-top:8px; display:inline-block;" href="{}">✓ Reactivate Account Now</a>'
                '</div>',
                reactivate_url
            )
        elif instance.is_locked:
            unlock_url = reverse('admin:user_unlock', args=[user.pk])
            return format_html(
                '<div style="background:#f8d7da; border:1px solid #f5c6cb; color:#721c24; padding:10px 14px; border-radius:6px; margin:4px 0 10px 0;">'
                '<strong>🔒 This account is LOCKED</strong> due to incorrect password attempts or security cooldown.<br>'
                '<a class="button" style="background:#fd7e14; color:white; padding:5px 16px; border-radius:4px; text-decoration:none; font-weight:bold; margin-top:8px; display:inline-block;" href="{}">🔓 Unlock Account Now</a>'
                '</div>',
                unlock_url
            )
        else:
            deactivate_url = reverse('admin:user_deactivate', args=[user.pk])
            return format_html(
                '<div style="background:#d1e7dd; border:1px solid #badbcc; color:#0f5132; padding:10px 14px; border-radius:6px; margin:4px 0 10px 0;">'
                '<strong>🟢 Account is ACTIVE.</strong> The user can freely log in and participate.<br>'
                '<a class="button" style="background:#dc3545; color:white; padding:4px 12px; border-radius:4px; text-decoration:none; margin-top:8px; display:inline-block; font-size:12px;" href="{}">Deactivate Account</a>'
                '</div>',
                deactivate_url
            )

    @admin.action(description='Reactivate selected user accounts (set active and unlock)')
    def activate_profiles(self, request, queryset):
        user_ids = list(queryset.values_list('user_id', flat=True))
        User.objects.filter(id__in=user_ids).update(is_active=True)
        updated = queryset.update(is_locked=False, failed_login_attempts=0, locked_at=None, unlock_at=None)
        if request:
            self.message_user(request, f"Successfully reactivated {len(user_ids)} user accounts.")

    @admin.action(description='Deactivate selected user accounts')
    def deactivate_profiles(self, request, queryset):
        user_ids = list(queryset.values_list('user_id', flat=True))
        count = User.objects.filter(id__in=user_ids).update(is_active=False)
        if request:
            self.message_user(request, f"Successfully deactivated {count} user accounts.")

    @admin.action(description='Unlock selected profiles (clear lock, cooldown & activate)')
    def unlock_accounts(self, request, queryset):
        user_ids = list(queryset.values_list('user_id', flat=True))
        User.objects.filter(id__in=user_ids).update(is_active=True)
        updated = queryset.update(is_locked=False, failed_login_attempts=0, locked_at=None, unlock_at=None)
        if request:
            self.message_user(request, f"Successfully unlocked and reactivated {updated} user profiles.")

    @admin.action(description='Lock selected profiles')
    def lock_accounts(self, request, queryset):
        updated = queryset.update(is_locked=True, locked_at=timezone.now())
        if request:
            self.message_user(request, f"Successfully locked {updated} user profiles.")

    @admin.action(description='Mark selected profiles as email-verified')
    def verify_emails(self, request, queryset):
        updated = queryset.update(email_verified=True)
        if request:
            self.message_user(request, f"Marked {updated} profiles as email-verified.")

    @admin.action(description='Mark selected profiles as unverified')
    def unverify_emails(self, request, queryset):
        updated = queryset.update(email_verified=False)
        if request:
            self.message_user(request, f"Marked {updated} profiles as unverified.")

    @admin.action(description='Reset failed login counters to 0')
    def reset_failed_attempts(self, request, queryset):
        updated = queryset.update(failed_login_attempts=0)
        if request:
            self.message_user(request, f"Reset failed login counters for {updated} profiles.")


