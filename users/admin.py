from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Student Profile, Security & Preferences'
    fk_name = 'user'
    fieldsets = (
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


class CustomUserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'get_department',
        'get_year',
        'get_email_verified',
        'get_is_locked',
        'is_staff',
        'is_active',
    )
    list_select_related = ('profile',)
    actions = [
        'unlock_selected_users',
        'lock_selected_users',
        'verify_selected_emails',
        'activate_selected_users',
        'deactivate_selected_users',
    ]

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

    @admin.display(description='Verified', boolean=True)
    def get_email_verified(self, instance):
        if hasattr(instance, 'profile'):
            return instance.profile.email_verified
        return False

    @admin.display(description='Locked', boolean=True)
    def get_is_locked(self, instance):
        if hasattr(instance, 'profile'):
            return instance.profile.is_locked
        return False

    @admin.action(description='Unlock selected user accounts (clear cooldown)')
    def unlock_selected_users(self, request, queryset):
        for user in queryset:
            if hasattr(user, 'profile'):
                user.profile.is_locked = False
                user.profile.failed_login_attempts = 0
                user.profile.locked_at = None
                user.profile.unlock_at = None
                user.profile.save()
        if request:
            self.message_user(request, f"Successfully unlocked {queryset.count()} user accounts.")

    @admin.action(description='Lock selected user accounts')
    def lock_selected_users(self, request, queryset):
        for user in queryset:
            if hasattr(user, 'profile'):
                user.profile.is_locked = True
                user.profile.locked_at = timezone.now()
                user.profile.save()
        if request:
            self.message_user(request, f"Successfully locked {queryset.count()} user accounts.")

    @admin.action(description='Mark selected users as email verified')
    def verify_selected_emails(self, request, queryset):
        for user in queryset:
            if hasattr(user, 'profile'):
                user.profile.email_verified = True
                user.profile.save()
        if request:
            self.message_user(request, f"Marked {queryset.count()} users as email verified.")

    @admin.action(description='Deactivate selected user accounts')
    def deactivate_selected_users(self, request, queryset):
        count = queryset.update(is_active=False)
        if request:
            self.message_user(request, f"Successfully deactivated {count} user accounts.")

    @admin.action(description='Reactivate selected user accounts')
    def activate_selected_users(self, request, queryset):
        count = queryset.update(is_active=True)
        if request:
            self.message_user(request, f"Successfully reactivated {count} user accounts.")


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'department',
        'year',
        'email_verified',
        'is_locked',
        'failed_login_attempts',
        'unlock_at',
        'show_on_leaderboard',
        'public_profile',
    )
    list_filter = (
        'email_verified',
        'is_locked',
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
    list_editable = ('email_verified', 'is_locked', 'show_on_leaderboard', 'public_profile')
    actions = ['unlock_accounts', 'lock_accounts', 'verify_emails', 'unverify_emails', 'reset_failed_attempts']
    fieldsets = (
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

    @admin.action(description='Unlock selected profiles (clear lock and cooldown)')
    def unlock_accounts(self, request, queryset):
        updated = queryset.update(is_locked=False, failed_login_attempts=0, locked_at=None, unlock_at=None)
        if request:
            self.message_user(request, f"Successfully unlocked {updated} user profiles.")

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


