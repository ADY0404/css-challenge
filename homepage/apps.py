from django.apps import AppConfig


class HomepageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'homepage'

    def ready(self):
        from django.contrib import admin
        from .admin_site import setup_custom_admin_dashboard
        setup_custom_admin_dashboard(admin.site)
