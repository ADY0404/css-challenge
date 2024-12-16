from django.shortcuts import render
from .models import Event
from collections import defaultdict

def activities(request):
    # Fetch events, ordered by descending date
    events = Event.objects.all().order_by('-date')
    
    # Group events by month and year
    grouped_events = defaultdict(list)
    for event in events:
        key = event.date.strftime('%B, %Y')  # Month, Year format
        grouped_events[key].append({
            "title": event.title,
            "description": event.description,
            "date": event.date.strftime('%d %B, %Y'),
            "image_url": event.image.url if event.image else None,
            "link": "#",  # You can customize links here
            "button_text": event.button_text,
        })
    
    return render(request, 'events/activities.html', {
        'grouped_events': dict(grouped_events)
    })
