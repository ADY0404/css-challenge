from django.contrib import admin
from .models import Executive


@admin.register(Executive)
class ExecutiveAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'academic_year', 'has_photo')
    list_filter = ('academic_year', 'position')
    search_fields = ('name', 'position', 'academic_year')
    list_editable = ('position', 'academic_year')
    ordering = ['academic_year', 'name']
    fieldsets = (
        ('Officer Details', {
            'fields': ('name', 'position', 'academic_year')
        }),
        ('Portrait Photo', {
            'fields': ('image',)
        }),
    )

    @admin.display(description='Has Photo', boolean=True)
    def has_photo(self, obj):
        return bool(obj.image)
