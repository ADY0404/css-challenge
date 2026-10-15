from django.db import models
from django.contrib.auth.models import User


class Challenge(models.Model):
    DIFFICULTY_CHOICES = [
        ('Beginner', 'Beginner Friendly'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]
    CATEGORY_CHOICES = [
        ('Design & Dev', 'Design & Development'),
        ('Build Log', 'Build Log & Systems'),
        ('Community', 'Community & Education'),
        ('Data Science', 'Data & Analytics'),
        ('Algorithms', 'Algorithms & Logic'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Design & Dev')
    difficulty = models.CharField(max_length=50, choices=DIFFICULTY_CHOICES, default='Beginner')
    summary = models.TextField()
    description = models.TextField()
    requirements = models.TextField(help_text="Deliverables and guidelines for this challenge")
    week_label = models.CharField(max_length=50, default='Week 04')
    deadline_text = models.CharField(max_length=100, default='Submit by Sunday')
    icon_class = models.CharField(max_length=50, default='bi-window-stack')
    art_class = models.CharField(max_length=50, default='art-purple')
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.title


class ChallengeSubmission(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenge_submissions')
    project_title = models.CharField(max_length=200)
    repo_url = models.URLField(help_text="GitHub or code repository URL")
    demo_url = models.URLField(blank=True, null=True, help_text="Optional live project URL")
    description = models.TextField(help_text="Short explanation of how you solved the problem")
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']
        unique_together = ('challenge', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.challenge.title}"


class SubmissionUpvote(models.Model):
    submission = models.ForeignKey(ChallengeSubmission, on_delete=models.CASCADE, related_name='upvotes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submission_upvotes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('submission', 'user')

    def __str__(self):
        return f"{self.user.username} upvoted {self.submission.project_title}"


def get_user_badges(user, rank=None):
    """Return a list of achievement badges earned by the user based on platform activity."""
    badges = []
    submissions_count = getattr(user, 'submission_count', None)
    if submissions_count is None:
        submissions_count = user.challenge_submissions.count()

    messages_count = getattr(user, 'message_count', None)
    if messages_count is None:
        messages_count = user.community_messages.count()

    if submissions_count >= 5:
        badges.append({
            'name': 'Frontend Master',
            'icon': 'bi-trophy-fill',
            'color': 'warning',
            'description': 'Submitted 5+ challenge solutions'
        })
    elif submissions_count >= 3:
        badges.append({
            'name': 'Code Craftsman',
            'icon': 'bi-award-fill',
            'color': 'primary',
            'description': 'Submitted 3+ challenge solutions'
        })
    elif submissions_count >= 1:
        badges.append({
            'name': 'First Solver',
            'icon': 'bi-check-circle-fill',
            'color': 'success',
            'description': 'Completed first society challenge'
        })

    if messages_count >= 5:
        badges.append({
            'name': 'Community Voice',
            'icon': 'bi-chat-heart-fill',
            'color': 'info',
            'description': 'Active contributor in discussion channels'
        })

    if rank and rank in (1, 2, 3):
        medal_colors = {1: 'warning', 2: 'secondary', 3: 'danger'}
        badges.append({
            'name': f'Top {rank} Ranked',
            'icon': 'bi-star-fill',
            'color': medal_colors.get(rank, 'primary'),
            'description': f'Rank #{rank} on the society leaderboard'
        })

    return badges


class Article(models.Model):
    CATEGORY_CHOICES = [
        ('learning', 'Learning'),
        ('community', 'Community'),
        ('career', 'Career'),
        ('build', 'Build Log'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='learning')
    author_name = models.CharField(max_length=100, default='CSS Editorial Team')
    author_role = models.CharField(max_length=100, default='CSS Contributor')
    read_time = models.CharField(max_length=50, default='5 min read')
    summary = models.TextField()
    content = models.TextField()
    image_path = models.CharField(max_length=200, default='images/AI.jpeg')
    is_featured = models.BooleanField(default=False)
    published_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', '-published_at']

    def __str__(self):
        return self.title


class Internship(models.Model):
    ROLE_TYPE_CHOICES = [
        ('Internship', 'Internship'),
        ('Part-time', 'Part-time'),
        ('Full-time', 'Full-time'),
    ]

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    role_type = models.CharField(max_length=50, choices=ROLE_TYPE_CHOICES, default='Internship')
    duration = models.CharField(max_length=50, default='12 weeks')
    description = models.TextField()
    requirements = models.TextField(blank=True, default='')
    tags = models.CharField(max_length=200, help_text="Comma-separated tags e.g. Python, React")
    apply_url = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    posted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', '-posted_at']

    def __str__(self):
        return f"{self.title} at {self.company}"

    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class CommunityMessage(models.Model):
    CHANNEL_CHOICES = [
        ('ai-ml', 'AI & Machine Learning'),
        ('web-cloud', 'Web & Cloud Systems'),
        ('cybersecurity', 'Cybersecurity & Ethical Hacking'),
        ('algorithms', 'Competitive Programming & Algorithms'),
        ('mobile', 'Mobile Apps & Engineering'),
        ('open-source', 'Open Source Collective'),
    ]

    channel = models.CharField(max_length=50, choices=CHANNEL_CHOICES, default='ai-ml')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='community_messages')
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='replies'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"[{self.channel}] {self.user.username}: {self.text[:30]}"


class ClinicAppointment(models.Model):
    SERVICE_CHOICES = [
        ('linux', 'Linux Dual-Boot & OS Setup (Ubuntu / Fedora / Debian)'),
        ('dev-env', 'Developer Environment Setup (Docker, Python, Git, C++, VS Code)'),
        ('hardware', 'Hardware Diagnostics, Thermal Paste & Fan Cleaning'),
        ('malware', 'Malware Removal, Bloatware Cleanup & Security Hardening'),
        ('general', 'General Laptop Troubleshooting & Driver Support'),
    ]

    SESSION_CHOICES = [
        ('2024-10-04', 'Wednesday, Oct 4, 2024 (2:00 PM – 5:30 PM) — Lab 204'),
        ('2024-10-06', 'Friday, Oct 6, 2024 (2:00 PM – 6:00 PM) — Lab 204'),
        ('2024-10-11', 'Wednesday, Oct 11, 2024 (2:00 PM – 5:30 PM) — Lab 204'),
        ('2024-10-13', 'Friday, Oct 13, 2024 (2:00 PM – 6:00 PM) — Lab 204'),
        ('2024-10-18', 'Wednesday, Oct 18, 2024 (2:00 PM – 5:30 PM) — Lab 204'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='clinic_appointments')
    ticket_id = models.CharField(max_length=30, unique=True, blank=True)
    full_name = models.CharField(max_length=150)
    student_email = models.EmailField()
    student_id = models.CharField(max_length=50, blank=True, default='')
    department = models.CharField(max_length=100, default='Computer Science')
    academic_year = models.CharField(max_length=20, default='Year 1')
    device_brand = models.CharField(max_length=100)
    device_model = models.CharField(max_length=100)
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES, default='linux')
    preferred_session = models.CharField(max_length=100, default='2024-10-04', help_text="Clinic session code or date")
    issue_description = models.TextField()
    backup_acknowledged = models.BooleanField(default=False)
    status = models.CharField(max_length=30, default='Confirmed')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.ticket_id} - {self.full_name} ({self.device_brand} {self.device_model})"

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            import uuid
            self.ticket_id = f"CLN-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)


class ClinicSession(models.Model):
    session_code = models.CharField(max_length=50, unique=True, help_text="Unique identifier e.g. 2024-10-04")
    date_title = models.CharField(max_length=120, help_text="e.g. Wednesday, Oct 4, 2024")
    time_slot = models.CharField(max_length=100, default="2:00 PM – 5:30 PM")
    venue = models.CharField(max_length=150, default="Software Lab 204, CS Building")
    focus_topic = models.CharField(max_length=255, default="Linux Dual-Boot & OS Installation")
    capacity = models.PositiveIntegerField(default=12)
    leads = models.CharField(max_length=200, default="Student Tech Leads")
    badge_text = models.CharField(max_length=80, blank=True, default="")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.date_title} ({self.time_slot}) - {self.venue}"


class InfoPage(models.Model):
    STATUS_CHOICES = [
        ('published', 'Published'),
        ('draft', 'Draft / Unpublished'),
    ]

    slug = models.SlugField(max_length=100, unique=True, help_text="Unique URL identifier e.g. school-of-groups, tell-your-story, community-guidelines")
    title = models.CharField(max_length=200)
    subtitle = models.TextField(blank=True, default='', help_text="Introductory text or subtitle for the page")
    summary = models.TextField(blank=True, default='', help_text="Short summary for meta/banner")
    badge_text = models.CharField(max_length=80, blank=True, default='', help_text="Badge above title e.g. Community Standards, Legal, Cohorts")
    hero_cta_text = models.CharField(max_length=100, blank=True, default='', help_text="Hero Call to Action button label")
    hero_cta_url = models.CharField(max_length=255, blank=True, default='', help_text="Hero Call to Action URL or path")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published', help_text="Publication state")
    is_published = models.BooleanField(default=True, help_text="Public visibility toggle. When false, only staff can preview.")
    effective_date = models.CharField(max_length=100, blank=True, default='', help_text="Effective date (e.g. October 2024)")
    contact_email = models.CharField(max_length=150, blank=True, default='', help_text="Contact email for inquiries or reports")
    body = models.TextField(blank=True, default='', help_text="Optional custom body/content to supplement template content.")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='modified_infopages')

    class Meta:
        ordering = ['title']
        verbose_name = "Managed Page"
        verbose_name_plural = "Managed Pages"

    def __str__(self):
        return f"{self.title} (/{self.slug}/)"

    def get_absolute_url(self):
        from django.urls import reverse
        named_routes = {
            'school-of-groups': 'school_of_groups',
            'tell-your-story': 'tell_your_story',
            'community-guidelines': 'community_guidelines',
            'guidelines': 'guidelines',
            'terms': 'terms',
            'privacy': 'privacy',
            'programs': 'programs',
        }
        if self.slug in named_routes:
            try:
                return reverse(named_routes[self.slug])
            except Exception:
                pass
        return f"/{self.slug}/"

    def create_version_snapshot(self, user=None, notes=''):
        """Create an immutable snapshot of this page and its sections."""
        next_ver = (self.versions.aggregate(models.Max('version_num'))['version_num__max'] or 0) + 1
        sections_data = [
            {
                'heading': s.heading,
                'section_key': s.section_key,
                'body': s.body,
                'icon_class': s.icon_class,
                'call_to_action_text': s.call_to_action_text,
                'call_to_action_url': s.call_to_action_url,
                'call_to_action_style': s.call_to_action_style,
                'order': s.order,
                'is_visible': s.is_visible,
            }
            for s in self.sections.all().order_by('order', 'id')
        ]
        return self.versions.create(
            version_num=next_ver,
            title=self.title,
            summary=self.summary,
            subtitle=self.subtitle,
            status=self.status,
            effective_date=self.effective_date,
            sections_snapshot=sections_data,
            saved_by=user,
            notes=notes or f"Snapshot v{next_ver} saved by {user.username if user else 'System'}",
        )

    def restore_version(self, version_id, restored_by=None):
        """Restore all content fields and sections from a selected PageVersion snapshot."""
        version = self.versions.get(id=version_id)
        self.title = version.title
        self.summary = version.summary
        self.subtitle = version.subtitle
        self.status = version.status
        self.is_published = (version.status == 'published')
        self.effective_date = version.effective_date
        self.last_modified_by = restored_by
        self.save()

        # Re-populate sections atomically
        self.sections.all().delete()
        for s_data in version.sections_snapshot:
            self.sections.create(
                heading=s_data.get('heading', ''),
                section_key=s_data.get('section_key', ''),
                body=s_data.get('body', ''),
                icon_class=s_data.get('icon_class', ''),
                call_to_action_text=s_data.get('call_to_action_text', ''),
                call_to_action_url=s_data.get('call_to_action_url', ''),
                call_to_action_style=s_data.get('call_to_action_style', 'btn-primary'),
                order=s_data.get('order', 0),
                is_visible=s_data.get('is_visible', True),
            )
        self.create_version_snapshot(
            user=restored_by,
            notes=f"Restored from version #{version.version_num} ({version.saved_at.strftime('%Y-%m-%d %H:%M')})"
        )


class PageSection(models.Model):
    CTA_STYLE_CHOICES = [
        ('btn-primary', 'Primary Solid (Blue)'),
        ('btn-outline-primary', 'Primary Outline'),
        ('btn-success', 'Success Solid (Green)'),
        ('btn-outline-success', 'Success Outline'),
        ('btn-secondary', 'Secondary Solid (Gray)'),
        ('btn-light', 'Light Button'),
    ]

    page = models.ForeignKey(InfoPage, on_delete=models.CASCADE, related_name='sections')
    heading = models.CharField(max_length=255)
    section_key = models.SlugField(max_length=100, blank=True, default='', help_text="Anchor slug for table of contents, e.g. 'code-of-conduct'")
    body = models.TextField(help_text="Section body text. Supports formatted paragraphs, lists, and safe HTML.")
    icon_class = models.CharField(max_length=80, blank=True, default='', help_text="Bootstrap icon e.g. bi-shield-check, bi-people")
    call_to_action_text = models.CharField(max_length=120, blank=True, default='', help_text="Optional CTA button text")
    call_to_action_url = models.CharField(max_length=255, blank=True, default='', help_text="Optional CTA URL or relative link")
    call_to_action_style = models.CharField(max_length=50, default='btn-primary', choices=CTA_STYLE_CHOICES)
    order = models.PositiveIntegerField(default=0, help_text="Display order (ascending)")
    is_visible = models.BooleanField(default=True, help_text="Show or hide this section on the public page")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Page Section"
        verbose_name_plural = "Page Sections"

    def __str__(self):
        return f"[{self.page.slug}] #{self.order} {self.heading}"

    @property
    def rendered_body(self):
        from .sanitizer import sanitize_html
        return sanitize_html(self.body)

    def save(self, *args, **kwargs):
        if not self.section_key and self.heading:
            from django.utils.text import slugify
            self.section_key = slugify(self.heading)[:100]
        super().save(*args, **kwargs)


class PageVersion(models.Model):
    page = models.ForeignKey(InfoPage, on_delete=models.CASCADE, related_name='versions')
    version_num = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True, default='')
    subtitle = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, default='published')
    effective_date = models.CharField(max_length=100, blank=True, default='')
    sections_snapshot = models.JSONField(default=list, help_text="Snapshot of sections data")
    saved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='page_versions')
    saved_at = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        ordering = ['-version_num', '-saved_at']
        unique_together = ('page', 'version_num')
        verbose_name = "Page Version"
        verbose_name_plural = "Page Versions"

    def __str__(self):
        return f"{self.page.slug} v{self.version_num} ({self.saved_at.strftime('%Y-%m-%d %H:%M')})"


# Proxy models for dedicated individual admin entries
class SchoolOfGroupsPage(InfoPage):
    class Meta:
        proxy = True
        verbose_name = "School of Groups"
        verbose_name_plural = "School of Groups"


class TellYourStoryPage(InfoPage):
    class Meta:
        proxy = True
        verbose_name = "Tell Your Story"
        verbose_name_plural = "Tell Your Story"


class CommunityGuidelinesPage(InfoPage):
    class Meta:
        proxy = True
        verbose_name = "Community Guidelines"
        verbose_name_plural = "Community Guidelines"


class GuidelinesPage(InfoPage):
    class Meta:
        proxy = True
        verbose_name = "Guidelines"
        verbose_name_plural = "Guidelines"


class TermsPage(InfoPage):
    class Meta:
        proxy = True
        verbose_name = "Terms"
        verbose_name_plural = "Terms"


class PrivacyPage(InfoPage):
    class Meta:
        proxy = True
        verbose_name = "Privacy"
        verbose_name_plural = "Privacy"



class CommunityChannel(models.Model):
    slug = models.SlugField(max_length=50, unique=True, help_text="e.g. ai-ml, web-cloud, cybersecurity")
    name = models.CharField(max_length=150, help_text="Channel name e.g. Future of AI & Machine Learning")
    description = models.TextField(help_text="Channel purpose and track overview")
    category = models.CharField(max_length=80, default="Technical Track")
    icon_class = models.CharField(max_length=80, default="bi-cpu-fill", help_text="Bootstrap icon e.g. bi-cpu-fill, bi-cloud-arrow-up-fill")
    accent_color = models.CharField(max_length=20, default="#2563EB", help_text="Hex color e.g. #4F46E5")
    accent_bg = models.CharField(max_length=20, default="#EEF2FF", help_text="Hex bg e.g. #EEF2FF")
    rail_class = models.CharField(max_length=30, default="rail-ai", help_text="Icon rail color class e.g. rail-ai, rail-web, rail-sec")
    image = models.ImageField(upload_to='community/channels/', blank=True, null=True, help_text="Hub icon or badge image (1:1 square, max 2MB)")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Community Channel"
        verbose_name_plural = "Community Channels"

    def __str__(self):
        return f"#{self.slug} - {self.name}"

    @property
    def category_key(self):
        slug_lower = self.slug.lower()
        cat_lower = (self.category or '').lower()
        if 'ai' in slug_lower or 'ai' in cat_lower or 'data' in cat_lower or 'machine' in cat_lower:
            return 'ai'
        if 'web' in slug_lower or 'cloud' in slug_lower or 'infra' in cat_lower or 'web' in cat_lower:
            return 'web'
        if 'sec' in slug_lower or 'cyber' in slug_lower or 'security' in cat_lower or 'hack' in cat_lower:
            return 'security'
        if 'algo' in slug_lower or 'problem' in cat_lower or 'icpc' in cat_lower or 'comp' in cat_lower:
            return 'algo'
        if 'mob' in slug_lower or 'app' in cat_lower or 'flutter' in cat_lower or 'ios' in cat_lower or 'android' in cat_lower:
            return 'mobile'
        if 'open' in slug_lower or 'sys' in slug_lower or 'linux' in cat_lower or 'git' in cat_lower or 'oss' in cat_lower:
            return 'systems'
        return 'all'


class SiteConfiguration(models.Model):
    site_name = models.CharField(max_length=150, default="Computer Science Society")
    site_logo = models.ImageField(upload_to='site_config/', blank=True, null=True, help_text="Site navbar logo (fallback: static/images/com.png)")
    hero_tagline = models.CharField(max_length=200, default="Official Student Chapter")
    hero_title = models.CharField(max_length=200, default="Computer Science Society")
    hero_description = models.TextField(
        default="Empowering students to learn, build, and lead in computing. Join specialized study cohorts, tackle hands-on weekly coding challenges, and connect with peer developers."
    )
    future_lab_image = models.ImageField(
        upload_to='site_config/',
        blank=True,
        null=True,
        help_text="Future Lab or Hero section photo (fallback: static/images/lab.jpg)"
    )
    future_lab_badge = models.CharField(
        max_length=150,
        default="Future Lab · Ideas Happen Here",
        help_text="Badge text overlaid on the Future Lab photo"
    )
    announcement_active = models.BooleanField(default=True, help_text="Show or hide the top site announcement banner")
    announcement_text = models.CharField(
        max_length=255,
        default="Upcoming CSS activities & workshops are now open for student registration!"
    )
    announcement_link_url = models.CharField(max_length=200, default="/activities/")
    announcement_link_text = models.CharField(max_length=60, default="View Events")
    contact_email = models.EmailField(default="css@knust.edu.gh")
    github_url = models.URLField(default="https://github.com", blank=True)
    linkedin_url = models.URLField(default="https://linkedin.com", blank=True)
    twitter_url = models.URLField(default="https://twitter.com", blank=True)
    instagram_url = models.URLField(default="https://instagram.com", blank=True)

    # Platform Security & Access Controls (Editable by Admin)
    recaptcha_enabled = models.BooleanField(default=True, help_text="Enable or disable Google reCAPTCHA v2 on forms")
    max_login_attempts = models.IntegerField(default=5, help_text="Number of failed logins before locking an account")
    lockout_duration_minutes = models.IntegerField(default=10, help_text="Cooldown duration in minutes after password reset")
    allow_user_registration = models.BooleanField(default=True, help_text="Allow new students to register on the platform")
    require_email_verification = models.BooleanField(
        default=True,
        help_text="Require email verification before regular users can log in (admins are exempt)"
    )

    # Core Pillars (Learn, Connect, Grow)
    pillar1_title = models.CharField(max_length=100, default="Learn")
    pillar1_description = models.TextField(
        default="Follow curated tracks from beginner syntax to production system architecture and cloud deployments."
    )
    pillar2_title = models.CharField(max_length=100, default="Connect")
    pillar2_description = models.TextField(
        default="Network with senior mentors, alumni engineers, and like-minded peers who share your career ambitions."
    )
    pillar3_title = models.CharField(max_length=100, default="Grow")
    pillar3_description = models.TextField(
        default="Expand your portfolio through hackathons, student tech clinics, and verified challenge submissions."
    )

    # Community Guidelines Banner
    guidelines_heading = models.CharField(max_length=200, default="Society Guidelines & Community Norms")
    guidelines_description = models.TextField(
        default="We maintain an inclusive, supportive, and harassment-free environment for all computer science students across all physical and digital spaces."
    )
    guidelines_button_text = models.CharField(max_length=80, default="Read Community Guidelines")

    # Challenges Highlight Section
    challenges_heading = models.CharField(max_length=200, default="Hands-on Coding Challenges")
    challenges_subheading = models.TextField(
        default="Sharpen your practical skills, build real projects, and showcase your code."
    )

    # Spotlight Section
    spotlight_heading = models.CharField(max_length=200, default="CSS Spotlight & Journal")
    spotlight_subheading = models.CharField(max_length=255, default="Insights, project writeups, and student reflections.")

    # Speaker Series / Student Stage Banner
    speaker_series_badge = models.CharField(max_length=80, default="Speaker Series")
    speaker_series_title = models.CharField(max_length=200, default="Tell Your Story · Bi-Weekly Student Stage")
    speaker_series_description = models.TextField(
        default="Hear how fellow CS students build notable projects, secure internships, and prepare for tech careers."
    )

    # Newsletter Box
    newsletter_heading = models.CharField(max_length=200, default="Subscribe to the CSS Newsletter")
    newsletter_subheading = models.CharField(
        max_length=255,
        default="Stay updated on weekly challenge releases, campus workshops, and internship openings."
    )

    # Homepage Activities Section Heading
    activities_heading = models.CharField(max_length=200, default="Upcoming Activities")
    activities_subheading = models.CharField(max_length=255, default="Workshops, study jams, and community sessions.")

    # Page Headers (Customise All Pages)
    activities_page_title = models.CharField(max_length=200, default="Activities & Events")
    activities_page_lead = models.TextField(default="Learn together, meet new people, and put your skills into practice.")

    challenges_page_title = models.CharField(max_length=200, default="Coding & Design Challenges")
    challenges_page_lead = models.TextField(default="Build real projects, solve engineering prompts, and showcase your GitHub repositories.")

    leaderboard_page_title = models.CharField(max_length=200, default="Society Leaderboard")
    leaderboard_page_lead = models.TextField(default="Top contributors, active challenge solvers, and community champions.")

    executives_page_title = models.CharField(max_length=200, default="Meet the Executives")
    executives_page_lead = models.TextField(default="These passionate leaders guide the society's mission, organize technical programs, foster partnerships, and champion initiatives that benefit our members.")

    blog_page_title = models.CharField(max_length=200, default="The CSS Journal")
    blog_page_lead = models.TextField(default="Tutorials, learning notes, engineering insights, and career stories from our student builders.")

    internships_page_title = models.CharField(max_length=200, default="Internships & Career Opportunities")
    internships_page_lead = models.TextField(default="Verified student roles, internships, and entry-level engineering opportunities shared with CSS members.")

    clinic_page_title = models.CharField(max_length=200, default="PC Clinic & Diagnostic Sessions")
    clinic_page_lead = models.TextField(default="Free hardware diagnostics, Linux dual-boot installations, developer environment setup, and thermal maintenance run by senior CS student technicians.")

    community_page_title = models.CharField(max_length=200, default="Join a Technical Community")
    community_page_lead = models.TextField(default="Explore specialized engineering tracks, participate in hands-on study groups, work on open-source projects, and accelerate your tech career alongside peer builders.")

    # Footer About Blurb
    footer_about_text = models.TextField(
        default="The official student computing organization supporting student engineers, developers, and researchers."
    )

    class Meta:
        verbose_name = "Site Configuration & Content"
        verbose_name_plural = "Site Configuration & Content"

    def __str__(self):
        return self.site_name

    @classmethod
    def get_solo(cls):
        config, _ = cls.objects.get_or_create(id=1)
        return config


