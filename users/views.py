from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from .models import Profile
from homepage.validators import validate_image_upload


def login_view(request):
    """Handle user authentication and sign in."""
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or username}!")
            next_url = request.GET.get('next')
            return redirect(next_url if next_url else "home")
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, "users/login.html")


def signup_view(request):
    """Handle new user registration with profile creation."""
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.year = form.cleaned_data.get("year")
            profile.save()
            login(request, user)
            messages.success(request, "Your account has been created. Welcome to CSS!")
            return redirect("home")
        messages.error(request, "Please correct the errors in the registration form below.")
    else:
        form = SignUpForm()
    return render(request, "users/signup.html", {"form": form})


@login_required
def update_profile(request):
    """Update member personal details, avatar, bio, and credentials."""
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            is_valid, error_msg = validate_image_upload(
                profile_picture,
                max_size_mb=2,
                min_width=100,
                min_height=100,
                max_width=2000,
                max_height=2000,
                target_aspect_ratio=1.0,
                aspect_ratio_tolerance=0.25,
                allowed_formats=('JPEG', 'PNG', 'WEBP')
            )
            if not is_valid:
                messages.error(request, error_msg)
                return redirect('profile')
            profile.profile_picture = profile_picture

        user.first_name = request.POST.get('first_name', user.first_name).strip()
        user.last_name = request.POST.get('last_name', user.last_name).strip()

        year = request.POST.get('year')
        if year:
            try:
                profile.year = int(year)
            except (ValueError, TypeError):
                pass

        profile.department = request.POST.get('department', profile.department).strip()
        profile.bio = request.POST.get('bio', profile.bio).strip()
        profile.github_url = request.POST.get('github_url', profile.github_url or '').strip() or None
        profile.linkedin_url = request.POST.get('linkedin_url', profile.linkedin_url or '').strip() or None

        password = request.POST.get('password', '').strip()
        password_changed = False
        if password:
            if len(password) < 6:
                messages.error(request, "New password must be at least 6 characters long.")
                return redirect('profile')
            user.password = make_password(password)
            password_changed = True

        user.save()
        profile.save()

        if password_changed:
            update_session_auth_hash(request, user)

        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('profile')

    return render(request, 'users/profile.html')


@login_required
def settings_view(request):
    """Manage notification, privacy, and account preferences."""
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'notifications':
            profile.email_digest = 'email_digest' in request.POST
            profile.challenge_notifications = 'challenge_notifications' in request.POST
            profile.internship_notifications = 'internship_notifications' in request.POST
            profile.community_mentions = 'community_mentions' in request.POST
            profile.save()
            messages.success(request, 'Your notification preferences have been saved.')
        elif action == 'privacy':
            profile.show_on_leaderboard = 'show_on_leaderboard' in request.POST
            profile.public_profile = 'public_profile' in request.POST
            profile.save()
            messages.success(request, 'Your community privacy settings have been updated.')
        return redirect('settings')

    return render(request, 'users/settings.html')


def member_profile(request, username):
    """View another member's public society profile, bio, links, and challenge portfolio."""
    member_user = get_object_or_404(User, username=username)
    member_profile, _ = Profile.objects.get_or_create(user=member_user)

    is_self = request.user.is_authenticated and request.user.id == member_user.id
    can_view = member_profile.public_profile or is_self or (request.user.is_authenticated and request.user.is_staff)

    if not can_view:
        return render(request, "users/private_profile.html", {"member_user": member_user, "is_self": is_self})

    submissions = member_user.challenge_submissions.select_related('challenge').order_by('-submitted_at')
    messages_count = member_user.community_messages.count()
    from homepage.models import get_user_badges
    badges = get_user_badges(member_user)

    context = {
        "member_user": member_user,
        "member_profile": member_profile,
        "submissions": submissions,
        "submissions_count": submissions.count(),
        "messages_count": messages_count,
        "badges": badges,
        "is_self": is_self,
    }
    return render(request, "users/member_profile.html", context)

