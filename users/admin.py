from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Society Profile & Preferences'
    fk_name = 'user'
    fieldsets = (
        ('Academic & Bio', {
            'fields': ('department', 'year', 'bio', 'profile_picture')
        }),
        ('Security & Status', {
            'fields': ('email_verified', 'is_locked', 'failed_login_attempts', 'locked_at', 'unlock_at')
        }),
        ('Social Links', {
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
        'get_year',
        'get_department',
        'is_active',
        'get_is_locked',
        'is_staff',
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
        'reactivate_selected_users',
        'deactivate_selected_users',
        'unlock_selected_users',
        'verify_selected_emails',
    ]

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Account Status & Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'description': 'Uncheck "Active" to deactivate this account, or check it to reactivate.',
        }),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

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

    @admin.display(description='Locked', boolean=True)
    def get_is_locked(self, instance):
        if hasattr(instance, 'profile'):
            return instance.profile.is_locked
        return False

    @admin.action(description='Reactivate selected user accounts')
    def reactivate_selected_users(self, request, queryset):
        user_ids = list(queryset.values_list('id', flat=True))
        User.objects.filter(id__in=user_ids).update(is_active=True)
        Profile.objects.filter(user_id__in=user_ids).update(
            is_locked=False,
            failed_login_attempts=0,
            locked_at=None,
            unlock_at=None,
        )
        if request:
            self.message_user(request, f"Successfully reactivated {len(user_ids)} account(s).")

    @admin.action(description='Deactivate selected user accounts')
    def deactivate_selected_users(self, request, queryset):
        count = queryset.update(is_active=False)
        if request:
            self.message_user(request, f"Successfully deactivated {count} account(s).")

    @admin.action(description='Unlock selected accounts (clear failed login lock)')
    def unlock_selected_users(self, request, queryset):
        user_ids = list(queryset.values_list('id', flat=True))
        User.objects.filter(id__in=user_ids).update(is_active=True)
        Profile.objects.filter(user_id__in=user_ids).update(
            is_locked=False,
            failed_login_attempts=0,
            locked_at=None,
            unlock_at=None,
        )
        if request:
            self.message_user(request, f"Successfully unlocked and reset {len(user_ids)} account(s).")

    @admin.action(description='Mark selected users as email-verified')
    def verify_selected_emails(self, request, queryset):
        user_ids = list(queryset.values_list('id', flat=True))
        count = Profile.objects.filter(user_id__in=user_ids).update(email_verified=True)
        if request:
            self.message_user(request, f"Marked {count} user profile(s) as email verified.")


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
        'get_is_active',
        'is_locked',
        'email_verified',
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
        'reactivate_profiles',
        'deactivate_profiles',
        'unlock_accounts',
        'verify_emails',
        'reset_failed_attempts',
    ]
    fieldsets = (
        ('Member Identification', {
            'fields': ('user', 'profile_picture')
        }),
        ('Security & Account Access Control', {
            'fields': ('email_verified', 'is_locked', 'failed_login_attempts', 'locked_at', 'unlock_at'),
            'description': 'To reactivate a deactivated user, use the Reactivate action or edit the User model.'
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

    @admin.display(description='Active', boolean=True)
    def get_is_active(self, instance):
        return instance.user.is_active if instance.user else False

    @admin.action(description='Reactivate selected user accounts')
    def reactivate_profiles(self, request, queryset):
        user_ids = list(queryset.values_list('user_id', flat=True))
        User.objects.filter(id__in=user_ids).update(is_active=True)
        queryset.update(is_locked=False, failed_login_attempts=0, locked_at=None, unlock_at=None)
        if request:
            self.message_user(request, f"Successfully reactivated {len(user_ids)} account(s).")

    @admin.action(description='Deactivate selected user accounts')
    def deactivate_profiles(self, request, queryset):
        user_ids = list(queryset.values_list('user_id', flat=True))
        count = User.objects.filter(id__in=user_ids).update(is_active=False)
        if request:
            self.message_user(request, f"Successfully deactivated {count} account(s).")

    @admin.action(description='Unlock selected user accounts (clear lock & reset attempts)')
    def unlock_accounts(self, request, queryset):
        user_ids = list(queryset.values_list('user_id', flat=True))
        User.objects.filter(id__in=user_ids).update(is_active=True)
        updated = queryset.update(is_locked=False, failed_login_attempts=0, locked_at=None, unlock_at=None)
        if request:
            self.message_user(request, f"Successfully unlocked {updated} profile(s).")

    unlock_profiles = unlock_accounts

    @admin.action(description='Mark selected profiles as email-verified')
    def verify_emails(self, request, queryset):
        updated = queryset.update(email_verified=True)
        if request:
            self.message_user(request, f"Marked {updated} profile(s) as email-verified.")

    @admin.action(description='Reset failed login counters to 0')
    def reset_failed_attempts(self, request, queryset):
        updated = queryset.update(failed_login_attempts=0)
        if request:
            self.message_user(request, f"Reset failed login counters for {updated} profile(s).")
