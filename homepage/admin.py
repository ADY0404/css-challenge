from django.contrib import admin
from .models import (
    Challenge,
    ChallengeSubmission,
    SubmissionUpvote,
    Article,
    Internship,
    NewsletterSubscriber,
    CommunityMessage,
    ClinicAppointment,
    ClinicSession,
    InfoPage,
    CommunityChannel,
    SiteConfiguration,
)


class SubmissionUpvoteInline(admin.TabularInline):
    model = SubmissionUpvote
    extra = 0
    readonly_fields = ('user', 'created_at')
    can_delete = True


class ChallengeSubmissionInline(admin.TabularInline):
    model = ChallengeSubmission
    extra = 0
    fields = ('user', 'project_title', 'repo_url', 'demo_url', 'submitted_at')
    readonly_fields = ('submitted_at',)
    can_delete = True
    show_change_link = True


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'difficulty',
        'week_label',
        'deadline_text',
        'is_featured',
        'is_active',
        'submissions_count',
        'created_at',
    )
    list_filter = ('category', 'difficulty', 'is_featured', 'is_active')
    search_fields = ('title', 'summary', 'description', 'requirements')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_featured', 'is_active')
    inlines = [ChallengeSubmissionInline]
    fieldsets = (
        ('Overview', {
            'fields': ('title', 'slug', 'category', 'difficulty', 'week_label', 'deadline_text')
        }),
        ('Details & Deliverables', {
            'fields': ('summary', 'description', 'requirements')
        }),
        ('Display & Styling', {
            'fields': ('icon_class', 'art_class', 'is_featured', 'is_active')
        }),
    )

    @admin.display(description='Submissions')
    def submissions_count(self, obj):
        return obj.submissions.count()


@admin.register(ChallengeSubmission)
class ChallengeSubmissionAdmin(admin.ModelAdmin):
    list_display = ('project_title', 'challenge', 'user', 'upvotes_count', 'repo_url', 'demo_url', 'submitted_at')
    list_filter = ('challenge', 'submitted_at')
    search_fields = ('project_title', 'user__username', 'user__email', 'repo_url', 'description')
    readonly_fields = ('submitted_at',)
    inlines = [SubmissionUpvoteInline]
    fieldsets = (
        ('Submission Info', {
            'fields': ('challenge', 'user', 'project_title', 'submitted_at')
        }),
        ('Links', {
            'fields': ('repo_url', 'demo_url')
        }),
        ('Approach & Solution Description', {
            'fields': ('description',)
        }),
    )

    @admin.display(description='Upvotes')
    def upvotes_count(self, obj):
        return obj.upvotes.count()


@admin.register(SubmissionUpvote)
class SubmissionUpvoteAdmin(admin.ModelAdmin):
    list_display = ('submission', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('submission__project_title', 'user__username')
    readonly_fields = ('created_at',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author_name', 'author_role', 'read_time', 'is_featured', 'published_at')
    list_filter = ('category', 'is_featured', 'published_at')
    search_fields = ('title', 'author_name', 'author_role', 'summary', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_featured',)
    fieldsets = (
        ('Article Info', {
            'fields': ('title', 'slug', 'category', 'read_time', 'image_path', 'is_featured')
        }),
        ('Author Byline', {
            'fields': ('author_name', 'author_role')
        }),
        ('Content', {
            'fields': ('summary', 'content')
        }),
    )


@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'role_type', 'duration', 'is_featured', 'posted_at')
    list_filter = ('role_type', 'is_featured', 'location')
    search_fields = ('title', 'company', 'location', 'tags', 'description', 'requirements')
    list_editable = ('is_featured',)
    fieldsets = (
        ('Role Overview', {
            'fields': ('title', 'company', 'location', 'role_type', 'duration', 'is_featured')
        }),
        ('Details', {
            'fields': ('description', 'requirements', 'tags', 'apply_url')
        }),
    )


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at',)


@admin.register(CommunityMessage)
class CommunityMessageAdmin(admin.ModelAdmin):
    list_display = ('channel', 'user', 'parent', 'short_text', 'created_at')
    list_filter = ('channel', 'created_at')
    search_fields = ('text', 'user__username', 'user__email')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Channel & Author', {
            'fields': ('channel', 'user', 'parent')
        }),
        ('Message Content', {
            'fields': ('text', 'created_at')
        }),
    )

    @admin.display(description='Message Preview')
    def short_text(self, obj):
        return (obj.text[:60] + '...') if len(obj.text) > 60 else obj.text


@admin.register(ClinicAppointment)
class ClinicAppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'ticket_id',
        'full_name',
        'student_email',
        'device_brand',
        'device_model',
        'service_type',
        'preferred_session',
        'status',
        'created_at',
    )
    list_filter = ('status', 'service_type', 'preferred_session', 'created_at')
    search_fields = ('ticket_id', 'full_name', 'student_email', 'student_id', 'device_brand', 'device_model', 'issue_description')
    list_editable = ('status',)
    readonly_fields = ('ticket_id', 'created_at')
    fieldsets = (
        ('Appointment Ticket', {
            'fields': ('ticket_id', 'status', 'preferred_session', 'service_type', 'created_at')
        }),
        ('Student Details', {
            'fields': ('user', 'full_name', 'student_email', 'student_id', 'department', 'academic_year')
        }),
        ('Device & Issue', {
            'fields': ('device_brand', 'device_model', 'issue_description', 'backup_acknowledged')
        }),
    )


@admin.register(ClinicSession)
class ClinicSessionAdmin(admin.ModelAdmin):
    list_display = (
        'date_title',
        'session_code',
        'time_slot',
        'venue',
        'capacity',
        'leads',
        'badge_text',
        'is_active',
        'order',
    )
    list_filter = ('is_active', 'venue')
    search_fields = ('date_title', 'session_code', 'venue', 'focus_topic', 'leads')
    list_editable = ('is_active', 'order')
    fieldsets = (
        ('Schedule', {
            'fields': ('session_code', 'date_title', 'time_slot', 'venue', 'order', 'is_active')
        }),
        ('Workshop Focus & Personnel', {
            'fields': ('focus_topic', 'capacity', 'leads', 'badge_text')
        }),
    )


@admin.register(InfoPage)
class InfoPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'summary_preview', 'updated_at')
    search_fields = ('title', 'slug', 'summary', 'body')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Page Identification', {
            'fields': ('title', 'slug')
        }),
        ('Summary Banner', {
            'fields': ('summary',)
        }),
        ('Body Content (Optional Override / Supplement)', {
            'fields': ('body',)
        }),
    )

    @admin.display(description='Summary Preview')
    def summary_preview(self, obj):
        return (obj.summary[:75] + '...') if len(obj.summary) > 75 else obj.summary


@admin.register(CommunityChannel)
class CommunityChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'icon_class', 'is_active', 'order')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'slug', 'description')
    list_editable = ('is_active', 'order')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Track Identity', {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('Visual Styling & Icons', {
            'fields': ('icon_class', 'accent_color', 'accent_bg', 'rail_class')
        }),
        ('Visibility & Ordering', {
            'fields': ('is_active', 'order')
        }),
    )


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'announcement_active', 'announcement_preview', 'contact_email')
    fieldsets = (
        ('Top Announcement Banner', {
            'fields': ('announcement_active', 'announcement_text', 'announcement_link_url', 'announcement_link_text')
        }),
        ('Branding & Hero Content', {
            'fields': ('site_name', 'hero_tagline', 'hero_title', 'hero_description')
        }),
        ('Contact & Social Media Links', {
            'fields': ('contact_email', 'github_url', 'linkedin_url', 'twitter_url', 'instagram_url')
        }),
    )

    @admin.display(description='Announcement')
    def announcement_preview(self, obj):
        return obj.announcement_text[:60] + '...' if len(obj.announcement_text) > 60 else obj.announcement_text

    def has_add_permission(self, request):
        # Only allow 1 singleton instance
        return not SiteConfiguration.objects.exists()
