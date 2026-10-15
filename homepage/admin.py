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
    PageSection,
    PageVersion,
    SchoolOfGroupsPage,
    TellYourStoryPage,
    CommunityGuidelinesPage,
    GuidelinesPage,
    TermsPage,
    PrivacyPage,
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


class PageSectionInline(admin.StackedInline):
    model = PageSection
    extra = 0
    fields = (
        ('heading', 'order', 'is_visible'),
        ('section_key', 'icon_class'),
        'body',
        ('call_to_action_text', 'call_to_action_url', 'call_to_action_style'),
    )
    prepopulated_fields = {'section_key': ('heading',)}


class PageVersionInline(admin.TabularInline):
    model = PageVersion
    extra = 0
    readonly_fields = ('version_num', 'saved_at', 'saved_by', 'status', 'sections_count', 'notes', 'restore_action')
    fields = ('version_num', 'saved_at', 'saved_by', 'status', 'sections_count', 'notes', 'restore_action')
    can_delete = False
    ordering = ('-version_num',)

    def has_add_permission(self, request, obj=None):
        return False

    @admin.display(description='Sections')
    def sections_count(self, obj):
        return len(obj.sections_snapshot) if obj.sections_snapshot else 0

    @admin.display(description='Restore')
    def restore_action(self, obj):
        return format_html(
            '<a class="button" style="background:#dc2626; color:white; padding:3px 10px; border-radius:4px; text-decoration:none;" href="/adcs/content/restore/{}/{}/">Restore v{}</a>',
            obj.page.slug,
            obj.id,
            obj.version_num
        )


@admin.register(InfoPage)
class InfoPageAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'status_badge',
        'is_published',
        'sections_count',
        'effective_date',
        'last_modified_by',
        'updated_at',
        'preview_link',
    )
    list_filter = ('status', 'is_published', 'updated_at')
    search_fields = ('title', 'slug', 'subtitle', 'summary', 'body')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PageSectionInline, PageVersionInline]
    actions = ['publish_pages', 'unpublish_pages', 'create_version_snapshot_action']

    fieldsets = (
        ('Page Identification & Branding', {
            'fields': ('title', 'slug', 'badge_text')
        }),
        ('Introductory Content & Summaries', {
            'fields': ('subtitle', 'summary')
        }),
        ('Publication Status & Visibility', {
            'fields': ('status', 'is_published', 'effective_date', 'contact_email')
        }),
        ('Hero Call to Action (Optional)', {
            'fields': ('hero_cta_text', 'hero_cta_url')
        }),
        ('Legacy / Fallback Content', {
            'fields': ('body',),
            'classes': ('collapse',),
            'description': 'Used only if no structured page sections are defined.'
        }),
    )

    @admin.display(description='Status')
    def status_badge(self, obj):
        if obj.status == 'published' and obj.is_published:
            return format_html('<span style="color:#15803d; font-weight:600;">&#10003; Published</span>')
        return format_html('<span style="color:#b45309; font-weight:600;">&#9998; Draft</span>')

    @admin.display(description='Sections')
    def sections_count(self, obj):
        return obj.sections.count()

    @admin.display(description='Preview')
    def preview_link(self, obj):
        url = obj.get_absolute_url()
        return format_html('<a href="{}" target="_blank" style="font-weight:600; text-decoration:none;">View &rarr;</a>', url)

    def save_model(self, request, obj, form, change):
        obj.last_modified_by = request.user
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.create_version_snapshot(
            user=request.user,
            notes=f"Updated by {request.user.get_full_name() or request.user.username}"
        )

    @admin.action(description="Publish selected pages")
    def publish_pages(self, request, queryset):
        count = queryset.update(status='published', is_published=True, last_modified_by=request.user)
        for page in queryset:
            page.create_version_snapshot(user=request.user, notes="Published via admin action")
        self.message_user(request, f"{count} page(s) published successfully.")

    @admin.action(description="Unpublish selected pages (Set to Draft)")
    def unpublish_pages(self, request, queryset):
        count = queryset.update(status='draft', is_published=False, last_modified_by=request.user)
        for page in queryset:
            page.create_version_snapshot(user=request.user, notes="Unpublished to Draft via admin action")
        self.message_user(request, f"{count} page(s) marked as Draft.")

    @admin.action(description="Create Version Snapshot for selected pages")
    def create_version_snapshot_action(self, request, queryset):
        for page in queryset:
            page.create_version_snapshot(user=request.user, notes="Manual snapshot via admin action")
        self.message_user(request, f"Created snapshots for {queryset.count()} page(s).")


class BaseSpecificPageAdmin(InfoPageAdmin):
    target_slug = ''

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if self.target_slug:
            return qs.filter(slug=self.target_slug)
        return qs

    def save_model(self, request, obj, form, change):
        if self.target_slug and not obj.slug:
            obj.slug = self.target_slug
        super().save_model(request, obj, form, change)


@admin.register(SchoolOfGroupsPage)
class SchoolOfGroupsPageAdmin(BaseSpecificPageAdmin):
    target_slug = 'school-of-groups'


@admin.register(TellYourStoryPage)
class TellYourStoryPageAdmin(BaseSpecificPageAdmin):
    target_slug = 'tell-your-story'


@admin.register(CommunityGuidelinesPage)
class CommunityGuidelinesPageAdmin(BaseSpecificPageAdmin):
    target_slug = 'community-guidelines'


@admin.register(GuidelinesPage)
class GuidelinesPageAdmin(BaseSpecificPageAdmin):
    target_slug = 'guidelines'


@admin.register(TermsPage)
class TermsPageAdmin(BaseSpecificPageAdmin):
    target_slug = 'terms'


@admin.register(PrivacyPage)
class PrivacyPageAdmin(BaseSpecificPageAdmin):
    target_slug = 'privacy'


@admin.register(PageSection)
class PageSectionAdmin(admin.ModelAdmin):
    list_display = ('heading', 'page', 'order', 'is_visible', 'call_to_action_text', 'updated_at')
    list_filter = ('page', 'is_visible')
    list_editable = ('order', 'is_visible')
    search_fields = ('heading', 'body', 'page__title')


@admin.register(PageVersion)
class PageVersionAdmin(admin.ModelAdmin):
    list_display = ('page', 'version_num', 'status', 'saved_by', 'saved_at', 'notes')
    list_filter = ('page', 'status', 'saved_at')
    search_fields = ('page__title', 'notes', 'saved_by__username')
    readonly_fields = ('page', 'version_num', 'title', 'summary', 'subtitle', 'status', 'effective_date', 'sections_snapshot', 'saved_by', 'saved_at', 'notes')



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
