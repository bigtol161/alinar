
import logging

def test_logging_view(request):
    logger = logging.getLogger(__name__)
    logger.error('ТЕСТОВОЕ СООБЩЕНИЕ ДЛЯ ПРОВЕРКИ ЛОГОВ')
    return HttpResponse('Проверка логирования')

