"""
Регистрация исполнителей.

Сценарий: новый исполнитель заводит аккаунт и сразу входит на сайт.
Защита от ботов двухступенчатая: скрытое поле-ловушка (honeypot) в форме
плюс лимит частоты отправок с одного IP (см. accounts/rate_limit.py).
"""

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from news.models import Lead
from orders.models import Notification, Order

from .forms import RegisterForm
from .rate_limit import rate_limit


@login_required
def profile(request):
    """Личный кабинет: данные аккаунта и карточки всех разделов пользователя."""
    user = request.user
    executor = getattr(user, 'executor', None)
    context = {
        'orders_count': Order.objects.filter(author=user).count(),
        'leads_count': user.leads.count(),
        'unread_count': Notification.objects.filter(recipient=user, is_read=False).count(),
        'executor': executor,
        'executor_leads_count': executor.leads.count() if executor else 0,
        'executor_leads_done': executor.leads.filter(status='done').count() if executor else 0,
    }
    return render(request, 'accounts/profile.html', context)


# Не больше 3 регистраций в час с одного IP — человеку хватает с запасом.
@rate_limit('register', limit=3, per=3600)
def register(request):
    """Регистрация нового пользователя с автоматическим входом после создания."""
    if request.user.is_authenticated:
        return redirect('news:home')

    if request.method == 'POST':
        if request.POST.get('website'):
            # Заполнил honeypot — значит бот. Молча делаем вид, что всё ок.
            return redirect('news:home')
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('news:home')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})
