from django.shortcuts import render, get_object_or_404
from .models import Event, GuestSpeaker, SocialMedia, Program
from collections import defaultdict
from django.utils.timezone import now  # Import this to handle timezone-aware dates

def activities(request):
    # Fetch events, ordered by descending date
    events = Event.objects.all().order_by('-date')
    
    # Group events by month and year
    grouped_events = defaultdict(list)
    for event in events:
        key = event.date.strftime('%B, %Y')  # Month, Year format
        grouped_events[key].append({
            "id": event.id,  # Add the event's id here
            "title": event.title,
            "description": event.description,
            "date": event.date.strftime('%d %B, %Y'),
            "image_url": event.image.url if event.image else None,
            "link": "#",  # This can be updated to use the id for dynamic linking
            "button_text": event.button_text,
        })
    
    return render(request, 'events/activities.html', {
        'grouped_events': dict(grouped_events)
    })


def event_detail(request, id):
    # Fetch the event by ID
    event = get_object_or_404(Event, id=id)

    # Fetch upcoming events, excluding the current event
    upcoming_events = Event.objects.filter(date__gte=now()).exclude(id=id)

    # Fetch guest speakers related to the event
    guest_speakers = GuestSpeaker.objects.filter(event=event)

    # Fetch other related data (if needed)
    social_links = SocialMedia.objects.all()
    programs = Program.objects.all()

    # Pass all the necessary data to the template
    context = {
        'event': event,
        'guest_speakers': guest_speakers,
        'upcoming_events': upcoming_events,
        'social_links': social_links,
        'programs': programs,
    }

    return render(request, 'events/event.html', context)


