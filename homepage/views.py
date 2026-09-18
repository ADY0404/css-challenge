from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.http import JsonResponse
from django.db import models
from django.db.models import Count, Q, Max
from django.utils.text import slugify
from django.contrib.auth.models import User
from .validators import validate_image_upload
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
    get_user_badges,
)
from activities.models import Event


def home(request):
    """Render dynamic homepage with real events, challenge spotlight, and articles."""
    today = timezone.now().date()
    upcoming_events = Event.objects.filter(date__gte=today).order_by('date')[:2]
    if not upcoming_events:
        upcoming_events = Event.objects.all().order_by('-date')[:2]

    featured_challenge = Challenge.objects.filter(is_featured=True, is_active=True).first()
    if not featured_challenge:
        featured_challenge = Challenge.objects.first()

    spotlight_articles = Article.objects.all()[:4]
    featured_article = spotlight_articles[0] if spotlight_articles else None
    recent_articles = spotlight_articles[1:] if len(spotlight_articles) > 1 else []

    context = {
        'upcoming_events': upcoming_events,
        'featured_challenge': featured_challenge,
        'featured_article': featured_article,
        'recent_articles': recent_articles,
    }
    return render(request, 'homepage/home.html', context)


# -----------------------------------------------------------------------------
# Challenges
# -----------------------------------------------------------------------------
def challenge_list(request):
    """List active challenges and display the featured weekly challenge."""
    challenges = Challenge.objects.filter(is_active=True)
    featured = challenges.filter(is_featured=True).first() or challenges.first()
    other_challenges = challenges.exclude(id=featured.id) if featured else challenges

    user_submissions = {}
    if request.user.is_authenticated:
        submissions = ChallengeSubmission.objects.filter(user=request.user)
        user_submissions = {s.challenge_id: s for s in submissions}

    context = {
        'featured_challenge': featured,
        'challenges': other_challenges,
        'user_submissions': user_submissions,
    }
    return render(request, 'homepage/challenge.html', context)


def challenge_detail(request, slug):
    """Display full challenge specification and accept project submissions."""
    challenge = get_object_or_404(Challenge, slug=slug)
    community_submissions = (
        challenge.submissions
        .select_related('user', 'user__profile')
        .annotate(num_upvotes=Count('upvotes'))
        .order_by('-num_upvotes', '-submitted_at')
    )

    user_submission = None
    user_upvoted_ids = set()
    if request.user.is_authenticated:
        user_submission = ChallengeSubmission.objects.filter(challenge=challenge, user=request.user).first()
        user_upvoted_ids = set(
            SubmissionUpvote.objects.filter(
                user=request.user,
                submission__challenge=challenge
            ).values_list('submission_id', flat=True)
        )

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "You must sign in to submit a challenge project.")
            return redirect(f"/login/?next=/challenges/{slug}/")

        project_title = request.POST.get('project_title', '').strip()
        repo_url = request.POST.get('repo_url', '').strip()
        demo_url = request.POST.get('demo_url', '').strip()
        description = request.POST.get('description', '').strip()

        if not project_title or not repo_url or not description:
            messages.error(request, "Please fill in the project title, repository URL, and description.")
        elif not (repo_url.startswith('http://') or repo_url.startswith('https://')):
            messages.error(request, "Please enter a valid URL starting with http:// or https:// for your repository.")
        else:
            sub, created = ChallengeSubmission.objects.update_or_create(
                challenge=challenge,
                user=request.user,
                defaults={
                    'project_title': project_title,
                    'repo_url': repo_url,
                    'demo_url': demo_url if (demo_url.startswith('http://') or demo_url.startswith('https://')) else None,
                    'description': description,
                }
            )
            verb = "submitted" if created else "updated"
            messages.success(request, f"Your project '{project_title}' has been successfully {verb}!")
            return redirect('challenge_detail', slug=slug)

    context = {
        'challenge': challenge,
        'submissions': community_submissions,
        'user_submission': user_submission,
        'user_upvoted_ids': user_upvoted_ids,
    }
    return render(request, 'homepage/challenge_detail.html', context)


@require_POST
def upvote_submission(request, sub_id):
    """Toggle upvote/like for a challenge solution via AJAX."""
    if not request.user.is_authenticated:
        return JsonResponse({
            'authenticated': False,
            'login_url': f"/login/?next={request.META.get('HTTP_REFERER', '/challenges/')}"
        }, status=401)

    submission = get_object_or_404(ChallengeSubmission, id=sub_id)
    existing_upvote = SubmissionUpvote.objects.filter(submission=submission, user=request.user).first()

    if existing_upvote:
        existing_upvote.delete()
        upvoted = False
    else:
        SubmissionUpvote.objects.create(submission=submission, user=request.user)
        upvoted = True

    count = submission.upvotes.count()
    return JsonResponse({
        'authenticated': True,
        'upvoted': upvoted,
        'count': count
    })


def leaderboard(request):
    """Render society challenge leaderboard with podium ranks, badges, and solver statistics."""
    ranked_users_qs = (
        User.objects.filter(is_active=True)
        .filter(Q(profile__show_on_leaderboard=True) | Q(profile__isnull=True))
        .annotate(
            submission_count=Count('challenge_submissions', distinct=True),
            message_count=Count('community_messages', distinct=True)
        )
        .filter(submission_count__gt=0)
        .select_related('profile')
        .order_by('-submission_count', 'date_joined')
    )

    ranked_members = []
    for idx, member in enumerate(ranked_users_qs, start=1):
        badges = get_user_badges(member, rank=idx)
        ranked_members.append({
            'rank': idx,
            'user': member,
            'submission_count': member.submission_count,
            'message_count': member.message_count,
            'badges': badges,
        })

    top_three = ranked_members[:3]
    rest_rankings = ranked_members[3:]

    total_challenges = Challenge.objects.filter(is_active=True).count()
    total_submissions = ChallengeSubmission.objects.count()
    total_participants = ranked_users_qs.count()

    context = {
        'ranked_members': ranked_members,
        'top_three': top_three,
        'rest_rankings': rest_rankings,
        'total_challenges': total_challenges,
        'total_submissions': total_submissions,
        'total_participants': total_participants,
    }
    return render(request, 'homepage/leaderboard.html', context)


# -----------------------------------------------------------------------------
# Blog / Journal
# -----------------------------------------------------------------------------
def blog_list(request):
    """List blog articles with category filtering."""
    category = request.GET.get('category', '').strip()
    articles = Article.objects.all()

    if category in ['learning', 'community', 'career', 'build']:
        articles = articles.filter(category=category)

    featured_story = articles.filter(is_featured=True).first() or articles.first()
    recent_stories = articles.exclude(id=featured_story.id) if featured_story else articles

    context = {
        'featured_story': featured_story,
        'recent_stories': recent_stories,
        'current_category': category,
    }
    return render(request, 'homepage/blog.html', context)


def article_detail(request, slug):
    """Render full blog article view."""
    article = get_object_or_404(Article, slug=slug)
    related_articles = Article.objects.filter(category=article.category).exclude(id=article.id)[:3]

    context = {
        'article': article,
        'related_articles': related_articles,
    }
    return render(request, 'homepage/article_detail.html', context)


# -----------------------------------------------------------------------------
# Internships
# -----------------------------------------------------------------------------
def internships_list(request):
    """Display open internship opportunities and career toolkit."""
    internships = Internship.objects.all()
    context = {
        'internships': internships,
    }
    return render(request, 'homepage/internships.html', context)


def share_opportunity(request):
    """Allow students and alumni to submit career opportunities."""
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        company = request.POST.get('company', '').strip()
        location = request.POST.get('location', '').strip()
        role_type = request.POST.get('role_type', 'Internship')
        description = request.POST.get('description', '').strip()
        apply_url = request.POST.get('apply_url', '').strip()
        tags = request.POST.get('tags', '').strip()

        if not title or not company or not location or not description:
            messages.error(request, "Please provide the role title, company, location, and description.")
        else:
            Internship.objects.create(
                title=title,
                company=company,
                location=location,
                role_type=role_type,
                description=description,
                apply_url=apply_url if (apply_url.startswith('http://') or apply_url.startswith('https://')) else None,
                tags=tags or 'Tech, Student Opportunity',
            )
            messages.success(request, f"Thank you! The opportunity at {company} has been posted to the CSS board.")
            return redirect('internships')

    return redirect('internships')


# -----------------------------------------------------------------------------
# Newsletter
# -----------------------------------------------------------------------------
def newsletter_subscribe(request):
    """Handle newsletter subscriptions across all templates."""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        try:
            validate_email(email)
            sub, created = NewsletterSubscriber.objects.get_or_create(email=email)
            if created:
                messages.success(request, "Thank you for subscribing to the CSS Journal & Society announcements!")
            else:
                messages.info(request, "You are already subscribed to the CSS newsletter.")
        except ValidationError:
            messages.error(request, "Please enter a valid email address.")

    referer = request.META.get('HTTP_REFERER')
    return redirect(referer if referer else 'home')


# -----------------------------------------------------------------------------
# Community & Channels
# -----------------------------------------------------------------------------
def get_active_channels():
    """Retrieve active community channels from DB or fallback dictionary."""
    db_channels = list(CommunityChannel.objects.filter(is_active=True).order_by('order', 'id'))
    if db_channels:
        channel_dict = {c.slug: c.name for c in db_channels}
        return channel_dict, db_channels
    fallback = {
        'ai-ml': 'Future of AI & Machine Learning',
        'web-cloud': 'Web & Cloud Systems Guild',
        'cybersecurity': 'Cybersecurity & Ethical Hacking',
        'algorithms': 'Competitive Programming & Algorithms',
        'mobile': 'Mobile Apps & Engineering',
        'open-source': 'Open Source Collective',
    }
    return fallback, []


def community(request):
    """Render community hub overview page with database-managed channels."""
    channels_dict, channels_list = get_active_channels()

    # Enrich channels with real participant profiles and activity counts
    for ch in channels_list:
        messages_qs = CommunityMessage.objects.filter(channel=ch.slug).select_related('user', 'user__profile')
        ch.message_count = messages_qs.count()
        recent_user_ids = []
        recent_users = []
        for msg in messages_qs.order_by('-created_at'):
            if msg.user.id not in recent_user_ids:
                recent_user_ids.append(msg.user.id)
                recent_users.append(msg.user)
            if len(recent_users) >= 4:
                break
        ch.recent_members = recent_users

    return render(request, 'homepage/community.html', {
        'channels': channels_list,
        'channels_dict': channels_dict,
    })


def propose_community_channel(request):
    """Handle student proposal of a new technical hub with image validation and persistence."""
    if request.method != 'POST':
        return redirect('community')

    if not request.user.is_authenticated:
        messages.error(request, "Please sign in to propose a new technical community hub.")
        return redirect(f"{reverse('login')}?next={reverse('community')}")

    name = request.POST.get('name', '').strip()
    category = request.POST.get('category', '').strip()
    description = request.POST.get('description', '').strip()
    hub_image = request.FILES.get('hub_image')

    # 1. Text field validations
    if not name or len(name) < 3:
        messages.error(request, "Please enter a valid hub title (at least 3 characters).")
        return redirect('community')

    if not description or len(description) < 15:
        messages.error(request, "Please provide a descriptive overview of the proposed track (at least 15 characters).")
        return redirect('community')

    # 2. Hub Image validation (1:1 square, min 100x100, max 1200x1200, PNG/JPG/WebP, max 2MB)
    if not hub_image:
        messages.error(request, "A square hub icon or cover image is required. Please select an image.")
        return redirect('community')

    is_valid, error_msg = validate_image_upload(
        hub_image,
        max_size_mb=2,
        min_width=100,
        min_height=100,
        max_width=1200,
        max_height=1200,
        target_aspect_ratio=1.0,
        aspect_ratio_tolerance=0.20,
        allowed_formats=('JPEG', 'PNG', 'WEBP')
    )
    if not is_valid:
        messages.error(request, error_msg)
        return redirect('community')

    # 3. Generate unique slug
    base_slug = slugify(name) or 'tech-track'
    slug = base_slug
    counter = 1
    while CommunityChannel.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    # 4. Map category to styling defaults
    cat_lower = category.lower()
    if 'ai' in cat_lower or 'machine' in cat_lower or 'data' in cat_lower:
        category_name = 'AI & Machine Learning'
        icon_class = 'bi-cpu-fill'
        accent_color = '#4F46E5'
        accent_bg = '#EEF2FF'
        rail_class = 'rail-ai'
    elif 'web' in cat_lower or 'cloud' in cat_lower:
        category_name = 'Web & Cloud'
        icon_class = 'bi-cloud-arrow-up-fill'
        accent_color = '#059669'
        accent_bg = '#ECFDF5'
        rail_class = 'rail-web'
    elif 'sec' in cat_lower or 'cyber' in cat_lower:
        category_name = 'Cybersecurity'
        icon_class = 'bi-shield-lock-fill'
        accent_color = '#DC2626'
        accent_bg = '#FEF2F2'
        rail_class = 'rail-sec'
    elif 'algo' in cat_lower or 'problem' in cat_lower:
        category_name = 'Algorithms & CP'
        icon_class = 'bi-diagram-3-fill'
        accent_color = '#D97706'
        accent_bg = '#FFFBEB'
        rail_class = 'rail-algo'
    elif 'mobile' in cat_lower or 'app' in cat_lower:
        category_name = 'Mobile Apps'
        icon_class = 'bi-phone-fill'
        accent_color = '#0284C7'
        accent_bg = '#F0F9FF'
        rail_class = 'rail-mobile'
    else:
        category_name = category or 'Open Source & Systems'
        icon_class = 'bi-git'
        accent_color = '#475569'
        accent_bg = '#F1F5F9'
        rail_class = 'rail-oss'

    # 5. Order calculation & creation
    max_order = CommunityChannel.objects.aggregate(Max('order'))['order__max'] or 0
    channel = CommunityChannel.objects.create(
        slug=slug,
        name=name,
        category=category_name,
        description=description,
        icon_class=icon_class,
        accent_color=accent_color,
        accent_bg=accent_bg,
        rail_class=rail_class,
        image=hub_image,
        is_active=True,
        order=max_order + 1,
    )

    messages.success(
        request,
        f"The '{name}' technical hub has been successfully created and added to the community directory!"
    )
    return redirect('community')


def community2(request, channel='ai-ml'):
    """Render active technical discussion channel with database persistence."""
    valid_channels, channels_list = get_active_channels()

    if channel not in valid_channels:
        channel = list(valid_channels.keys())[0] if valid_channels else 'ai-ml'

    current_channel_obj = next((c for c in channels_list if c.slug == channel), None)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "You must be signed in to post in community channels.")
            return redirect(f"{reverse('login')}?next={reverse('community_channel', kwargs={'channel': channel})}")

        text = request.POST.get('text', '').strip()
        parent_id = request.POST.get('parent_id', '').strip()
        parent_msg = None
        if parent_id and parent_id.isdigit():
            parent_msg = CommunityMessage.objects.filter(id=int(parent_id), channel=channel).first()

        if text:
            CommunityMessage.objects.create(
                channel=channel,
                user=request.user,
                text=text,
                parent=parent_msg,
            )
            return redirect('community_channel', channel=channel)

    channel_messages = (
        CommunityMessage.objects.filter(channel=channel)
        .select_related('user', 'user__profile', 'parent', 'parent__user')
        .order_by('created_at')
    )

    context = {
        'active_channel': channel,
        'channel_title': valid_channels.get(channel, channel),
        'channels': valid_channels,
        'channels_list_obj': channels_list,
        'current_channel_obj': current_channel_obj,
        'messages_list': channel_messages,
    }
    return render(request, 'homepage/community2.html', context)


def community_messages_api(request):
    """JSON API endpoint returning recent messages after after_id for real-time polling."""
    channel = request.GET.get('channel', 'ai-ml')
    after_id = request.GET.get('after_id', '0')
    try:
        after_id = int(after_id)
    except ValueError:
        after_id = 0

    new_messages = (
        CommunityMessage.objects.filter(channel=channel, id__gt=after_id)
        .select_related('user', 'user__profile', 'parent', 'parent__user')
        .order_by('created_at')
    )

    items = []
    for msg in new_messages:
        avatar_url = None
        if hasattr(msg.user, 'profile') and msg.user.profile.profile_picture:
            try:
                avatar_url = msg.user.profile.profile_picture.url
            except Exception:
                avatar_url = None

        initial = (msg.user.first_name[:1] or msg.user.username[:1] or 'U').upper()
        department = msg.user.profile.department if hasattr(msg.user, 'profile') and msg.user.profile.department else ''

        items.append({
            'id': msg.id,
            'username': msg.user.username,
            'full_name': msg.user.get_full_name() or msg.user.username,
            'avatar_url': avatar_url,
            'initial': initial,
            'department': department,
            'created_at': msg.created_at.strftime('%b %d, %I:%M %p').replace(' 0', ' '),
            'text': msg.text,
            'parent_id': msg.parent.id if msg.parent else None,
            'parent_author': (msg.parent.user.get_full_name() or msg.parent.user.username) if msg.parent else None,
            'parent_snippet': msg.parent.text[:55] if msg.parent else None,
        })

    return JsonResponse({'messages': items})


# -----------------------------------------------------------------------------
# Informational Pages
# -----------------------------------------------------------------------------
INFO_PAGES = {
    'guidelines': {
        'title': 'Society Guidelines',
        'summary': 'Be respectful, inclusive, and constructive. These principles help keep CSS a welcoming place to learn and collaborate.',
    },
    'programs': {
        'title': 'CSS Programs',
        'summary': 'Explore society programs including School of Groups, Tell Your Story, PC Clinic, and Hackathons.',
    },
    'terms': {
        'title': 'Terms of Use',
        'summary': 'Use CSS community spaces responsibly and respect the privacy, work, and time of other members.',
    },
    'privacy': {
        'title': 'Privacy',
        'summary': 'CSS uses the information you provide to operate your account and deliver society activities.',
    },
}


def info_page(request, page):
    """Render informational pages (guidelines, programs, terms, privacy) backed by InfoPage model."""
    db_page = InfoPage.objects.filter(slug=page).first()
    if db_page:
        context = {
            'title': db_page.title,
            'summary': db_page.summary,
            'body': db_page.body,
            'page_key': page,
            'updated_at': db_page.updated_at,
        }
    else:
        page_data = INFO_PAGES.get(page, {'title': page.capitalize(), 'summary': ''})
        context = dict(page_data)
        context['page_key'] = page
    return render(request, 'homepage/info_page.html', context)


# -----------------------------------------------------------------------------
# PC Clinic Dates & Appointments
# -----------------------------------------------------------------------------
def clinic_dates(request):
    """Render PC Clinic session dates, services guide, and handle student appointment requests."""
    db_sessions = ClinicSession.objects.filter(is_active=True).order_by('order', 'id')
    if db_sessions.exists():
        sessions_data = [
            {
                'id': s.session_code,
                'date': s.date_title,
                'time': s.time_slot,
                'venue': s.venue,
                'focus': s.focus_topic,
                'capacity': s.capacity,
                'leads': s.leads,
                'badge': s.badge_text or ('Next Upcoming Session' if idx == 0 else 'Open for Booking'),
                'badge_class': 'bg-success' if (s.badge_text == 'Next Upcoming Session' or idx == 0) else 'bg-primary',
                'is_open': True,
            }
            for idx, s in enumerate(db_sessions)
        ]
    else:
        sessions_data = [
            {
                'id': '2024-10-04',
                'date': 'Wednesday, Oct 4, 2024',
                'time': '2:00 PM – 5:30 PM',
                'venue': 'Software Lab 204, CS Building',
                'focus': 'Linux Dual-Boot & OS Installation (Ubuntu 24.04 LTS / Fedora 40)',
                'capacity': 12,
                'leads': 'David Koomson & Zainab Adeleke',
                'badge': 'Next Upcoming Session',
                'badge_class': 'bg-success',
                'is_open': True,
            },
            {
                'id': '2024-10-06',
                'date': 'Friday, Oct 6, 2024',
                'time': '2:00 PM – 6:00 PM',
                'venue': 'Software Lab 204, CS Building',
                'focus': 'Developer Toolchains & IDEs (Docker, VS Code, Git/SSH, Python, GCC)',
                'capacity': 12,
                'leads': 'Emmanuel Tetteh & Peer Mentors',
                'badge': 'Open for Booking',
                'badge_class': 'bg-primary',
                'is_open': True,
            },
            {
                'id': '2024-10-11',
                'date': 'Wednesday, Oct 11, 2024',
                'time': '2:00 PM – 5:30 PM',
                'venue': 'Software Lab 204, CS Building',
                'focus': 'Hardware Diagnostics, Thermal Servicing & Fan De-dusting',
                'capacity': 12,
                'leads': 'David Koomson & Hardware Guild',
                'badge': 'Open for Booking',
                'badge_class': 'bg-primary',
                'is_open': True,
            },
            {
                'id': '2024-10-13',
                'date': 'Friday, Oct 13, 2024',
                'time': '2:00 PM – 6:00 PM',
                'venue': 'Software Lab 204, CS Building',
                'focus': 'Malware Removal, System Cleanup & Disk Security Hardening',
                'capacity': 12,
                'leads': 'Cybersecurity Guild Team',
                'badge': 'Open for Booking',
                'badge_class': 'bg-primary',
                'is_open': True,
            },
            {
                'id': '2024-10-18',
                'date': 'Wednesday, Oct 18, 2024',
                'time': '2:00 PM – 5:30 PM',
                'venue': 'Software Lab 204, CS Building',
                'focus': 'General Laptop Diagnostics & Driver Troubleshooting',
                'capacity': 12,
                'leads': 'CSS Systems Volunteer Team',
                'badge': 'Open for Booking',
                'badge_class': 'bg-primary',
                'is_open': True,
            },
        ]

    for s in sessions_data:
        booked = ClinicAppointment.objects.filter(preferred_session=s['id']).count()
        s['booked_count'] = booked
        s['available_slots'] = max(0, s['capacity'] - booked)
        if s['available_slots'] == 0:
            s['badge'] = 'Session Full (Waitlist)'
            s['badge_class'] = 'bg-secondary'
            s['is_open'] = False

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        student_email = request.POST.get('student_email', '').strip().lower()
        student_id = request.POST.get('student_id', '').strip()
        department = request.POST.get('department', '').strip() or 'Computer Science'
        academic_year = request.POST.get('academic_year', '').strip() or 'Year 1'
        device_brand = request.POST.get('device_brand', '').strip()
        device_model = request.POST.get('device_model', '').strip()
        service_type = request.POST.get('service_type', 'linux')
        preferred_session = request.POST.get('preferred_session', '2024-10-04')
        issue_description = request.POST.get('issue_description', '').strip()
        backup_acknowledged = 'backup_acknowledged' in request.POST

        if not full_name or not student_email or not device_brand or not device_model or not issue_description:
            messages.error(request, "Please fill in all required fields (Name, Email, Device, and Issue Description).")
        else:
            try:
                validate_email(student_email)
                appointment = ClinicAppointment.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    full_name=full_name,
                    student_email=student_email,
                    student_id=student_id,
                    department=department,
                    academic_year=academic_year,
                    device_brand=device_brand,
                    device_model=device_model,
                    service_type=service_type,
                    preferred_session=preferred_session,
                    issue_description=issue_description,
                    backup_acknowledged=backup_acknowledged,
                )
                messages.success(
                    request,
                    f"Clinic slot requested! Your Ticket ID is {appointment.ticket_id}. "
                    f"Please bring your {device_brand} {device_model} and charger to Room 204 on your session date."
                )
                return redirect('clinic_dates')
            except ValidationError:
                messages.error(request, "Please enter a valid student email address.")

    user_appointments = []
    if request.user.is_authenticated:
        user_appointments = ClinicAppointment.objects.filter(user=request.user)

    context = {
        'sessions': sessions_data,
        'user_appointments': user_appointments,
    }
    return render(request, 'homepage/clinic_dates.html', context)


def search(request):
    """Global search across challenges, blog articles, internships, and community discussions."""
    query = request.GET.get('q', '').strip()
    tab = request.GET.get('tab', 'all')

    challenges = []
    articles = []
    internships = []
    community_messages = []

    if query:
        challenges = list(
            Challenge.objects.filter(
                Q(title__icontains=query) |
                Q(summary__icontains=query) |
                Q(description__icontains=query) |
                Q(category__icontains=query)
            ).distinct()
        )

        articles = list(
            Article.objects.filter(
                Q(title__icontains=query) |
                Q(summary__icontains=query) |
                Q(content__icontains=query) |
                Q(author_name__icontains=query)
            ).distinct()
        )

        internships = list(
            Internship.objects.filter(
                Q(title__icontains=query) |
                Q(company__icontains=query) |
                Q(location__icontains=query) |
                Q(tags__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
        )

        community_messages = list(
            CommunityMessage.objects.filter(text__icontains=query)
            .select_related('user', 'user__profile')
            .order_by('-created_at')[:25]
        )

    challenges_count = len(challenges)
    articles_count = len(articles)
    internships_count = len(internships)
    messages_count = len(community_messages)
    total_results = challenges_count + articles_count + internships_count + messages_count

    context = {
        'query': query,
        'tab': tab,
        'challenges': challenges,
        'articles': articles,
        'internships': internships,
        'community_messages': community_messages,
        'total_results': total_results,
        'challenges_count': challenges_count,
        'articles_count': articles_count,
        'internships_count': internships_count,
        'messages_count': messages_count,
    }
    return render(request, 'homepage/search_results.html', context)

