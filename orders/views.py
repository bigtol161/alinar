from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import OrderForm, ResponseForm
from accounts.rate_limit import rate_limit
from core.models import City, Service
from django.db.models import Count
from .models import Notification, Order


def order_list(request):
    """Список заказов: активные по умолчанию, закрытые по ?status=closed,
    поиск по названию через ?q=."""
    status = 'closed' if request.GET.get('status') == 'closed' else 'new'
    q = request.GET.get('q', '').strip()
    city_id = request.GET.get('city', '')
    service_id = request.GET.get('service', '')
    orders = Order.objects.filter(status=status).select_related('city', 'service')
    if q:
        orders = orders.filter(title__icontains=q)
    if city_id.isdigit():
        orders = orders.filter(city_id=city_id)
    if service_id.isdigit():
        orders = orders.filter(service_id=service_id)
    orders = orders.order_by('-created_at')
    page = Paginator(orders, 10).get_page(request.GET.get('page'))

    qs = request.GET.copy()
    qs.pop('page', None)
    qs.pop('status', None)
    base_qs = qs.urlencode()
    qs.pop('q', None)
    base_qs_nostatus = qs.urlencode()

    context = {
        'page_obj': page, 'status': status, 'q': q,
        'base_qs': base_qs, 'base_qs_nostatus': base_qs_nostatus,
        'cities': City.objects.all().order_by('name'),
        'services': Service.objects.all().order_by('name'),
    }
    return render(request, 'orders/order_list.html', context)


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
    q = request.GET.get('q', '').strip()
    city_id = request.GET.get('city', '')
    service_id = request.GET.get('service', '')
    orders = (
        request.user.orders
        .select_related('city', 'service')
        .annotate(responses_count=Count('responses'))
    )
    if q:
        orders = orders.filter(title__icontains=q)
    if city_id.isdigit():
        orders = orders.filter(city_id=city_id)
    if service_id.isdigit():
        orders = orders.filter(service_id=service_id)
    orders = orders.order_by('-created_at')
    page = Paginator(orders, 10).get_page(request.GET.get('page'))

    qs = request.GET.copy()
    qs.pop('page', None)
    base_qs = qs.urlencode()

    context = {
        'page_obj': page, 'q': q, 'base_qs': base_qs,
        'cities': City.objects.all().order_by('name'),
        'services': Service.objects.all().order_by('name'),
    }
    return render(request, 'orders/my_orders.html', context)


@login_required
@login_required
def notifications(request):
    """Список уведомлений текущего пользователя."""
    notes = (
        request.user.notifications
        .select_related('order', 'response', 'response__executor')
        .order_by('-created_at')
    )
    page = Paginator(notes, 20).get_page(request.GET.get('page'))
    return render(request, 'orders/notifications.html', {'page_obj': page})


@login_required
def notifications_read(request):
    """Отметить все уведомления пользователя прочитанными (только POST)."""
    if request.method != 'POST':
        return redirect('orders:notifications')
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return redirect('orders:notifications')


def order_close(request, pk):
    """Закрыть заказ может только его автор."""
    order = get_object_or_404(Order, pk=pk)
    if order.author_id == request.user.pk:
        order.status = 'closed'
        order.save(update_fields=('status',))
        for resp in order.responses.select_related('executor'):
            user = getattr(resp.executor, 'user', None)
            if user is None:
                continue
            Notification.objects.get_or_create(
                kind=Notification.KIND_CLOSED,
                recipient=user,
                response=resp,
                defaults={'order': order},
            )
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
            Notification.objects.create(
                recipient=order.author,
                order=order,
                response=response,
            )
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

