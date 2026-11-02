import time

from django.core.cache import cache
from django.http import HttpResponse


def rate_limit(key, limit=5, per=3600):
    """Не больше limit POST-запросов с одного IP за per секунд."""
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            if request.method == 'POST':
                ip = request.META.get('REMOTE_ADDR', '')
                k = f'rl:{key}:{ip}'
                now = time.time()
                hits = [t for t in cache.get(k, []) if now - t < per]
                if len(hits) >= limit:
                    return HttpResponse('Слишком много попыток. Попробуйте позже.')
                hits.append(now)
                cache.set(k, hits, per)
            return view(request, *args, **kwargs)
        return wrapper
    return decorator
