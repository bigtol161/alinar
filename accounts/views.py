from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


def register(request):
    """Регистрация нового пользователя с автоматическим входом после создания."""
    if request.user.is_authenticated:
        return redirect('news:home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('news:home')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})
