"""
Регистрация исполнителей.

Сценарий: новый исполнитель заводит аккаунт и сразу входит на сайт.
Защита от ботов двухступенчатая: скрытое поле-ловушка (honeypot) в форме
плюс лимит частоты отправок с одного IP (см. accounts/rate_limit.py).
"""

from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import RegisterForm
from .rate_limit import rate_limit


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
