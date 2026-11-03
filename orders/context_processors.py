"""Контекст-процессоры приложения заказов."""


def unread_notifications(request):
    """Счётчик непрочитанных уведомлений для колокольчика в шапке."""
    count = 0
    if request.user.is_authenticated:
        count = request.user.notifications.filter(is_read=False).count()
    return {'unread_count': count}
