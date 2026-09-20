from django.conf import settings
from .models import SiteConfiguration


def site_settings(request):
    """Expose society site configuration and content to all templates."""
    try:
        config = SiteConfiguration.get_solo()
    except Exception:
        config = None

    recaptcha_enabled = getattr(settings, 'RECAPTCHA_ENABLED', True)
    if config and hasattr(config, 'recaptcha_enabled'):
        recaptcha_enabled = config.recaptcha_enabled and recaptcha_enabled

    return {
        'site_config': config,
        'RECAPTCHA_SITE_KEY': getattr(settings, 'RECAPTCHA_SITE_KEY', ''),
        'RECAPTCHA_ENABLED': recaptcha_enabled,
    }


