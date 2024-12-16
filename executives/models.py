from django.db import models

# Create your models here.

# from django.db import models

# class Executive(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     date = models.DateField()
#     image_url = models.ImageField(upload_to='events/images/', blank=True, null=True)
#     link = models.URLField(blank=True, null=True)

#     def __str__(self):
#         return self.title
    
from django.db import models

class Executive(models.Model):
    name = models.CharField(max_length=255)  # Ensure this field exists
    position = models.CharField(max_length=255)
    academic_year = models.CharField(max_length=50)  # Ensure this field exists
    image = models.ImageField(upload_to='events/images/', blank=True, null=True)

    def __str__(self):
        return self.name


