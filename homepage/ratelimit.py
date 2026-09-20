import functools
import time
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse


def get_client_ip(request):
    """
    Extract client IP address respecting reverse proxies like Render.
    Uses the first address in HTTP_X_FORWARDED_FOR or falls back to REMOTE_ADDR.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '127.0.0.1')


def ratelimit(rate='5/m', action=None, methods=('POST',)):
    """
    Sliding-window rate-limiting decorator backed by Django's native cache.
    rate format: 'count/period' where period is 's' (seconds), 'm' (minutes),
    'h' (hours), or 'd' (days). Example: '5/m', '3/h'.
    """
    count_str, period_str = rate.split('/')
    max_requests = int(count_str)
    period_map = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
    window = period_map.get(period_str.lower(), 60)

    def decorator(view_func):
        @functools.wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if getattr(settings, 'RATELIMIT_ENABLE', True) and request.method in methods:
                ip = get_client_ip(request)
                act = action or f"{view_func.__module__}.{view_func.__name__}"
                cache_key = f"rl:{act}:{ip}"

                now = time.time()
                history = cache.get(cache_key, [])
                history = [ts for ts in history if now - ts < window]

                if len(history) >= max_requests:
                    retry_after = int(window - (now - history[0])) if history else window
                    response = HttpResponse(
                        f"Too many requests from this IP. Please try again in {max(1, retry_after)} seconds.",
                        status=429,
                    )
                    response['Retry-After'] = str(max(1, retry_after))
                    return response

                history.append(now)
                cache.set(cache_key, history, timeout=window)

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator

