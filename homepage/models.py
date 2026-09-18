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
    slug = models.SlugField(max_length=50, unique=True, help_text="guidelines, programs, terms, or privacy")
    title = models.CharField(max_length=150)
    summary = models.TextField(blank=True, default='')
    body = models.TextField(blank=True, default='', help_text="Optional custom body/content to supplement template content.")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['slug']

    def __str__(self):
        return f"{self.title} (/{self.slug}/)"


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
    hero_tagline = models.CharField(max_length=200, default="Official Student Chapter")
    hero_title = models.CharField(max_length=200, default="Computer Science Society")
    hero_description = models.TextField(
        default="Empowering students to learn, build, and lead in computing. Join specialized study cohorts, tackle hands-on weekly coding challenges, and connect with peer developers."
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

    class Meta:
        verbose_name = "Site Configuration & Content"
        verbose_name_plural = "Site Configuration & Content"

    def __str__(self):
        return self.site_name

    @classmethod
    def get_solo(cls):
        config, _ = cls.objects.get_or_create(id=1)
        return config


