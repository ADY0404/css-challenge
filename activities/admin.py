from django.contrib import admin
from .models import Event, GuestSpeaker, SocialMedia, Program, EventRegistration


class GuestSpeakerInline(admin.TabularInline):
    model = GuestSpeaker
    extra = 1
    fields = ('name', 'title', 'image_url')
    show_change_link = True


class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 0
    fields = ('full_name', 'email', 'year', 'registered_at')
    readonly_fields = ('registered_at',)
    can_delete = True
    show_change_link = True


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'date',
        'time',
        'button_text',
        'speakers_count',
        'registrations_count',
    )
    list_filter = ('date',)
    search_fields = ('title', 'description', 'activity')
    list_editable = ('button_text',)
    inlines = [GuestSpeakerInline, EventRegistrationInline]
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'date', 'time', 'button_text')
        }),
        ('Descriptions & Program', {
            'fields': ('description', 'activity')
        }),
        ('Event Media', {
            'fields': ('image', 'banner_image')
        }),
    )

    @admin.display(description='Speakers')
    def speakers_count(self, obj):
        return obj.guestspeaker_set.count()

    @admin.display(description='RSVPs')
    def registrations_count(self, obj):
        return obj.registrations.count()


@admin.register(GuestSpeaker)
class GuestSpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'event')
    list_filter = ('event',)
    search_fields = ('name', 'title')
    list_editable = ('title',)


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'get_year', 'event', 'registered_at')
    list_filter = ('event', 'year', 'registered_at')
    search_fields = ('full_name', 'email', 'notes', 'user__username')
    readonly_fields = ('registered_at',)
    fieldsets = (
        ('Attendee Details', {
            'fields': ('event', 'user', 'full_name', 'email', 'year', 'registered_at')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
    )

    @admin.display(description='Year')
    def get_year(self, obj):
        return obj.year_display


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ('platform', 'link')
    search_fields = ('platform', 'link')
    list_editable = ('link',)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'link')
    search_fields = ('name', 'link')
    list_editable = ('link',)