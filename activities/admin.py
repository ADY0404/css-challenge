from django.contrib import admin
from .models import Event

# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'button_text')  # Displayed fields
    search_fields = ('title', 'description')  # Searchable fields
    list_filter = ('date',)  # Filters for the sidebar
