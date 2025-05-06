from django.contrib import admin
from .models import Event, GuestSpeaker

# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')  # Displayed fields
    search_fields = ('title', 'description')  # Searchable fields
    list_filter = ('date',)  # Filters for the sidebar

@admin.register(GuestSpeaker)
class GuestSpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'title')

# @admin.register(activity)