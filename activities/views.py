from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Event, GuestSpeaker, SocialMedia, Program, EventRegistration
from collections import defaultdict
from django.utils.timezone import now


SAMPLE_EVENTS = [
    {'slug': 'web-development-workshop', 'title': 'Web Development Workshop', 'description': 'Build a responsive portfolio page and learn practical HTML, CSS, and Git workflows.', 'date': '18 October 2026 · 10:00 AM', 'month': 'October 2026', 'image_path': 'images/gat.jpeg', 'button_text': 'View workshop'},
    {'slug': 'career-conversations', 'title': 'Career Conversations', 'description': 'Meet industry guests and hear practical advice on internships, portfolios, and early careers.', 'date': '5 November 2026 · 2:00 PM', 'month': 'November 2026', 'image_path': 'images/bot.jpeg', 'button_text': 'View session'},
    {'slug': 'ai-study-jam', 'title': 'AI Study Jam', 'description': 'A collaborative introduction to machine learning concepts, tools, and responsible AI.', 'date': '21 November 2026 · 11:00 AM', 'month': 'November 2026', 'image_path': 'images/AI.jpeg', 'button_text': 'View study jam'},
]


def activities(request):
    """List all society activities grouped by month and year."""
    events = Event.objects.all().order_by('date')

    grouped_events = defaultdict(list)
    for event in events:
        key = event.date.strftime('%B, %Y')
        grouped_events[key].append({
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "date": event.date.strftime('%d %B, %Y'),
            "image_url": event.image.url if event.image else (event.banner_image.url if event.banner_image else None),
            "button_text": event.button_text or "View Event",
        })

    if grouped_events:
        return render(request, 'events/activities.html', {
            'grouped_events': dict(grouped_events),
            'showing_sample_events': False,
        })

    sample_events = defaultdict(list)
    for event in SAMPLE_EVENTS:
        sample_events[event['month']].append(event)
    return render(request, 'events/activities.html', {
        'grouped_events': dict(sample_events),
        'showing_sample_events': True,
    })


def event_detail(request, id):
    """Display single event with guest speakers, outline, and registration form."""
    event = get_object_or_404(Event, id=id)
    upcoming_events = Event.objects.filter(date__gte=now().date()).exclude(id=id).order_by('date')[:3]
    guest_speakers = GuestSpeaker.objects.filter(event=event)
    social_links = SocialMedia.objects.all()
    programs = Program.objects.all()

    user_registered = False
    if request.user.is_authenticated:
        user_registered = EventRegistration.objects.filter(event=event, user=request.user).exists()

    context = {
        'event': event,
        'guest_speakers': guest_speakers,
        'upcoming_events': upcoming_events,
        'social_links': social_links,
        'programs': programs,
        'user_registered': user_registered,
    }
    return render(request, 'events/event.html', context)


def event_register(request, id):
    """Process event registration and persist attendee in database."""
    event = get_object_or_404(Event, id=id)

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        year_str = request.POST.get('year', '1')

        try:
            year = int(year_str)
        except (ValueError, TypeError):
            year = 1

        if not full_name or not email:
            messages.error(request, "Please enter your full name and student email address.")
            return redirect('act:event', id=id)

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Please enter a valid email address.")
            return redirect('act:event', id=id)

        user = request.user if request.user.is_authenticated else None
        reg, created = EventRegistration.objects.get_or_create(
            event=event,
            email=email,
            defaults={
                'full_name': full_name,
                'year': year,
                'user': user,
            }
        )

        if created:
            messages.success(request, f"Registration confirmed! You are registered for '{event.title}'.")
        else:
            messages.info(request, f"You are already registered for '{event.title}' with {email}.")

    return redirect('act:event', id=id)


def sample_event_detail(request, slug):
    """Fallback sample event page if real database events are not being used."""
    event = next((e for e in SAMPLE_EVENTS if e['slug'] == slug), None)
    if event is None:
        raise Http404('Sample event not found.')
    return render(request, 'events/sample_event.html', {'event': event})
