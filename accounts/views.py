from django.contrib.auth import login
from .forms import RegisterForm
from django.shortcuts import redirect, render


def register(request):
    """Регистрация нового пользователя с автоматическим входом после создания."""
    if request.user.is_authenticated:
        return redirect('news:home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('news:home')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})
