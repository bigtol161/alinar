from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import OrderForm, ResponseForm
from accounts.rate_limit import rate_limit
from .models import Order


def order_list(request):
    """Открытые заказы — видят все, включая анонимов."""
    orders = (
        Order.objects.filter(status='new')
        .select_related('city', 'service')
        .order_by('-created_at')
    )
    page = Paginator(orders, 10).get_page(request.GET.get('page'))
    return render(request, 'orders/order_list.html', {'page_obj': page})


def order_detail(request, pk):
    """Страница заказа. Отклики с телефонами видит только автор заказа."""
    order = get_object_or_404(Order, pk=pk)

    is_author = request.user.is_authenticated and order.author_id == request.user.pk
    executor = None
    can_respond = False
    if request.user.is_authenticated:
        executor = getattr(request.user, 'executor', None)
        can_respond = (
            executor is not None
            and not is_author
            and order.status == 'new'
            and not order.responses.filter(executor=executor).exists()
        )

    responses = order.responses.select_related('executor__city') if is_author else order.responses.none()
    already_responded = (
        request.user.is_authenticated
        and executor is not None
        and order.responses.filter(executor=executor).exists()
    )

    return render(request, 'orders/order_detail.html', {
        'order': order,
        'responses': responses,
        'is_author': is_author,
        'can_respond': can_respond,
        'already_responded': already_responded,
        'form': ResponseForm() if can_respond else None,
    })


@login_required
@rate_limit('order', limit=5, per=3600)
def order_create(request):
    """Разместить заказ может только зарегистрированный пользователь."""
    if request.method == 'POST':
        if request.POST.get('website'):
            # Заполнил honeypot — бот; показываем пустую форму снова
            return render(request, 'orders/order_form.html', {'form': OrderForm()})
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.author = request.user
            order.save()
            return redirect('orders:mine')
    else:
        form = OrderForm()

    return render(request, 'orders/order_form.html', {'form': form})


@login_required
def my_orders(request):
    """Заказы текущего пользователя."""
    orders = request.user.orders.select_related('city', 'service')
    return render(request, 'orders/my_orders.html', {'orders': orders})


@login_required
def order_close(request, pk):
    """Закрыть заказ может только его автор."""
    order = get_object_or_404(Order, pk=pk)
    if order.author_id == request.user.pk:
        order.status = 'closed'
        order.save(update_fields=('status',))
    return redirect('orders:mine')


@login_required
@rate_limit('response', limit=20, per=3600)
def order_respond(request, pk):
    """Откликнуться может только мастер с привязанной анкетой,
    на открытый заказ, чужой и один раз."""
    order = get_object_or_404(Order, pk=pk)
    executor = getattr(request.user, 'executor', None)

    if (
        executor is None
        or order.status != 'new'
        or order.author_id == request.user.pk
        or order.responses.filter(executor=executor).exists()
    ):
        return redirect('orders:detail', pk=order.pk)

    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.order = order
            response.executor = executor
            response.save()
            return redirect('orders:detail', pk=order.pk)
    else:
        form = ResponseForm()

    return render(request, 'orders/order_detail.html', {
        'order': order,
        'responses': order.responses.none(),
        'is_author': False,
        'can_respond': True,
        'already_responded': False,
        'form': form,
    })

