"""
Защита форм от спама: ограничение частоты отправок (rate limit).

Как работает:
- на каждый POST-запрос запоминаем IP отправителя в кэше Django;
- если с одного IP за последний час пришло больше допустимого числа
  отправок — отдаём короткий отказ «Слишком много попыток» вместо
  обработки формы;
- GET-запросы (просто посмотреть страницу) не считаются: лимит давит
  на отправки, а не на просмотр.

Почему так: боты шлют десятки запросов в минуту с одного адреса,
живой человек столько форм не заполняет. Данные храним в кэше проекта
(settings.CACHES) — отдельная таблица в базе не нужна.
"""

import time

from django.core.cache import cache
from django.http import HttpResponse


def rate_limit(key, limit=5, per=3600):
    """Декоратор: не больше limit POST-запросов с одного IP за per секунд.

    key — уникальное имя лимита ('register', 'lead', 'order'): разные
    формы считаются независимо и не вымещают друг друга.
    """
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            if request.method == 'POST':
                ip = request.META.get('REMOTE_ADDR', '')
                k = f'rl:{key}:{ip}'
                now = time.time()
                # Оставляем только отметки времени внутри окна per секунд.
                hits = [t for t in cache.get(k, []) if now - t < per]
                if len(hits) >= limit:
                    return HttpResponse('Слишком много попыток. Попробуйте позже.')
                hits.append(now)
                cache.set(k, hits, per)
            return view(request, *args, **kwargs)
        return wrapper
    return decorator
