
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

def test_log_view(request):
    logger.error('ТЕСТОВОЕ СООБЩЕНИЕ ДЛЯ ПРОВЕРКИ ЛОГОВ')
    return HttpResponse('Проверка логирования')

