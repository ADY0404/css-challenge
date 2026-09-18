from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    department = models.CharField(max_length=120, blank=True, default='Computer Science')
    bio = models.TextField(blank=True, default='')
    github_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)

    # Notification preferences
    email_digest = models.BooleanField(default=True)
    challenge_notifications = models.BooleanField(default=True)
    internship_notifications = models.BooleanField(default=True)
    community_mentions = models.BooleanField(default=False)

    # Privacy preferences
    show_on_leaderboard = models.BooleanField(default=True)
    public_profile = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username