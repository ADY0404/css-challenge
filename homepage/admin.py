from django.contrib import admin
from django.utils.html import format_html
from django.templatetags.static import static
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
    list_display = (
        'site_name',
        'announcement_active',
        'recaptcha_enabled',
        'require_email_verification',
        'allow_user_registration',
        'max_login_attempts',
        'lockout_duration_minutes',
        'contact_email',
    )
    readonly_fields = ('future_lab_image_preview', 'site_logo_preview')

    fieldsets = (
        ('Top Announcement Banner', {
            'fields': ('announcement_active', 'announcement_text', 'announcement_link_url', 'announcement_link_text')
        }),
        ('Platform Security & Access Controls', {
            'fields': (
                'recaptcha_enabled',
                'require_email_verification',
                'allow_user_registration',
                'max_login_attempts',
                'lockout_duration_minutes',
            ),
            'description': 'Configure platform-wide security policies, Google reCAPTCHA, and student registration.'
        }),
        ('Branding & Site Logo', {
            'fields': (
                'site_name',
                'site_logo',
                'site_logo_preview',
            ),
            'description': 'Configure society title and brand mark displayed in the navigation and headers.'
        }),
        ('Hero Section & Future Lab Picture', {
            'fields': (
                'hero_tagline',
                'hero_title',
                'hero_description',
                'future_lab_image',
                'future_lab_image_preview',
                'future_lab_badge',
            ),
            'description': 'Customise the main homepage hero banner, including the Future Lab photograph and badge caption.'
        }),
        ('Core Pillars (Learn, Connect, Grow)', {
            'fields': (
                ('pillar1_title', 'pillar1_description'),
                ('pillar2_title', 'pillar2_description'),
                ('pillar3_title', 'pillar3_description'),
            ),
            'description': 'Configure the three core pillars displayed on the homepage.'
        }),
        ('Homepage Activities Section', {
            'fields': ('activities_heading', 'activities_subheading'),
            'description': 'Customise the heading and description for the upcoming activities preview on the homepage.'
        }),
        ('Page Headers (Customise All Main Pages)', {
            'fields': (
                ('activities_page_title', 'activities_page_lead'),
                ('challenges_page_title', 'challenges_page_lead'),
                ('leaderboard_page_title', 'leaderboard_page_lead'),
                ('executives_page_title', 'executives_page_lead'),
                ('blog_page_title', 'blog_page_lead'),
                ('internships_page_title', 'internships_page_lead'),
                ('clinic_page_title', 'clinic_page_lead'),
                ('community_page_title', 'community_page_lead'),
            ),
            'description': 'Customise the page title and subtitle lead for each top-level public page.'
        }),
        ('Community Guidelines Banner', {
            'fields': ('guidelines_heading', 'guidelines_description', 'guidelines_button_text')
        }),
        ('Challenges Highlight Section (Homepage)', {
            'fields': ('challenges_heading', 'challenges_subheading')
        }),
        ('CSS Spotlight & Journal Section', {
            'fields': ('spotlight_heading', 'spotlight_subheading')
        }),
        ('Student Speaker Series Banner', {
            'fields': ('speaker_series_badge', 'speaker_series_title', 'speaker_series_description')
        }),
        ('Newsletter Subscription Box', {
            'fields': ('newsletter_heading', 'newsletter_subheading')
        }),
        ('Contact, Social Links & Footer', {
            'fields': ('footer_about_text', 'contact_email', 'github_url', 'linkedin_url', 'twitter_url', 'instagram_url')
        }),
    )

    @admin.display(description="Future Lab Image Preview")
    def future_lab_image_preview(self, obj):
        if obj and obj.future_lab_image:
            img_url = obj.future_lab_image.url
            caption = "Custom uploaded Future Lab image active."
        else:
            img_url = static('images/lab.jpg')
            caption = "Default Future Lab image active (/static/images/lab.jpg). Upload a new photo above to replace it."
        return format_html(
            '<div style="margin-top: 6px;">'
            '<img src="{}" alt="Future Lab Preview" style="max-height: 220px; max-width: 380px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.15); display: block; margin-bottom: 6px;" />'
            '<span style="font-size: 0.82rem; color: #64748b; font-weight: 500;">{}</span>'
            '</div>',
            img_url,
            caption
        )

    @admin.display(description="Site Logo Preview")
    def site_logo_preview(self, obj):
        if obj and obj.site_logo:
            img_url = obj.site_logo.url
            caption = "Custom uploaded logo active."
        else:
            img_url = static('images/com.png')
            caption = "Default CSS logo active (/static/images/com.png). Upload a new logo above to replace it."
        return format_html(
            '<div style="margin-top: 6px;">'
            '<img src="{}" alt="Site Logo Preview" style="max-height: 60px; object-fit: contain; background: #f8fafc; padding: 6px; border: 1px solid #e2e8f0; border-radius: 8px; display: block; margin-bottom: 6px;" />'
            '<span style="font-size: 0.82rem; color: #64748b; font-weight: 500;">{}</span>'
            '</div>',
            img_url,
            caption
        )

    @admin.display(description='Announcement')
    def announcement_preview(self, obj):
        return obj.announcement_text[:60] + '...' if len(obj.announcement_text) > 60 else obj.announcement_text

    def has_add_permission(self, request):
        # Only allow 1 singleton instance
        return not SiteConfiguration.objects.exists()
