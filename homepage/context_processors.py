from .models import SiteConfiguration


def site_settings(request):
    """Expose society site configuration and content to all templates."""
    try:
        return {'site_config': SiteConfiguration.get_solo()}
    except Exception:
        return {'site_config': None}

