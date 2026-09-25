from django.db import models

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=200)
    time = models.TimeField()
    description = models.TextField()
    activity = models.TextField()  # You can still use this field if you want to store general activities info
    date = models.DateField()
    image = models.ImageField(upload_to='activities/')
    banner_image = models.ImageField(upload_to='events/images/')
    button_text = models.CharField(max_length=50, default="VIEW EVENT")

    def __str__(self):
        return self.title

# class Activity(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.TextField()
#     event = models.ForeignKey(Event, related_name='activities', on_delete=models.CASCADE)  # This links Activity to Event

#     def __str__(self):
#         return self.name

# class Event(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     date = models.DateField()
#     time = models.TimeField()
#     location = models.CharField(max_length=200)
#     image_url = models.ImageField(upload_to='events/')
#     link = models.URLField(blank=True, null=True)

#     def __str__(self):
#         return self.title


class GuestSpeaker(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    image_url = models.ImageField(upload_to='guest_speakers/')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SocialMedia(models.Model):
    platform = models.CharField(max_length=50)  # e.g., Instagram, LinkedIn
    link = models.URLField()

    def __str__(self):
        return self.platform


class Program(models.Model):
    name = models.CharField(max_length=100)
    link = models.URLField()

    def __str__(self):
        return self.name


class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='event_registrations')
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    year = models.IntegerField(default=1)
    notes = models.TextField(blank=True, default='')
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-registered_at']
        unique_together = ('event', 'email')

    def __str__(self):
        return f"{self.full_name} ({self.email}) - {self.event.title}"

    @property
    def year_display(self):
        if self.year == 5:
            return "Postgrad"
        return f"Year {self.year}"