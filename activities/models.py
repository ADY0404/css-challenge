from django.db import models

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    image = models.ImageField(upload_to='activities/')
    button_text = models.CharField(max_length=50, default="VIEW EVENT")
    
    def __str__(self):
        return self.title
