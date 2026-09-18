from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Student Profile & Preferences'
    fk_name = 'user'
    fieldsets = (
        ('Academic & Bio', {
            'fields': ('department', 'year', 'bio', 'profile_picture')
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
        'is_staff',
        'is_active',
    )
    list_select_related = ('profile',)

    @admin.display(description='Department')
    def get_department(self, instance):
        if hasattr(instance, 'profile'):
            return instance.profile.department
        return '-'

    @admin.display(description='Year')
    def get_year(self, instance):
        if hasattr(instance, 'profile') and instance.profile.year:
            return f"Year {instance.profile.year}"
        return '-'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'department',
        'year',
        'show_on_leaderboard',
        'public_profile',
        'email_digest',
    )
    list_filter = (
        'department',
        'year',
        'show_on_leaderboard',
        'public_profile',
        'email_digest',
    )
    search_fields = (
        'user__username',
        'user__email',
        'user__first_name',
        'user__last_name',
        'department',
        'bio',
    )
    list_editable = ('show_on_leaderboard', 'public_profile')
    fieldsets = (
        ('Member', {
            'fields': ('user', 'profile_picture')
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
