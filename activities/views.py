from django.shortcuts import render
from .models import Event
from collections import defaultdict
from datetime import datetime

# Create your views here.

def activities(request):
    # Fetch all events from the database, ordered by date in descending order
    events = Event.objects.all().order_by('-date')
    
    # Group events by month and year
    grouped_events = defaultdict(list)
    for event in events:
        # Format the date as "Month, Year"
        key = event.date.strftime('%B, %Y')
        grouped_events[key].append({
            "title": event.title,
            "description": event.description,
            "date": event.date.strftime('%d %B, %Y'),
            "image_url": event.image_url.url if event.image_url else "/static/images/default.jpg",  # Use a default image if none is provided
            "link": event.link if event.link else "#",
        })

    # Pass the grouped events to the template
    return render(request, 'events/activities.html', {'grouped_events': dict(grouped_events)})
