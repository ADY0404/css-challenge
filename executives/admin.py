from django.contrib import admin
from .models import Executive

# Register your models here.

@admin.register(Executive)
class ExecutiveAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'academic_year')

