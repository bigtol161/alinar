from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from core.models import City, Service
from orders.models import Order
from .forms import LeadForm
from accounts.rate_limit import rate_limit
from orders.models import Notification
from .models import Article, Executor, Lead



def home(request):
    """Главная страница: поиск, города, популярные услуги, свежие статьи и заказы."""
    articles = Article.objects.filter(is_published=True)[:6]
    cities = (
        City.objects
        .annotate(
            num_articles=Count('articles', filter=Q(articles__is_published=True)),
            num_executors=Count('executors', filter=Q(executors__is_active=True)),
        )
        .filter(num_articles__gt=0)
    )
    current_rubric = request.GET.get('rubric') or ''
    popular_services = (
        Service.objects
        .annotate(num_executors=Count('executors', filter=Q(executors__is_active=True)))
        .filter(num_executors__gt=0)
    )
    if current_rubric:
        popular_services = popular_services.filter(rubric=current_rubric)
    popular_services = popular_services[:8]
    fresh_orders = (
        Order.objects.filter(status='new')
        .select_related('city', 'service')[:3]
    )
    context = {
        'articles': articles,
        'cities': cities,
        'popular_services': popular_services,
        'rubrics': Service.RUBRIC_CHOICES,
        'current_rubric': current_rubric,
        'fresh_orders': fresh_orders,
        'total': Article.objects.filter(is_published=True).count(),
        'masters': Executor.objects.filter(is_active=True).count(),
        # Счётчик показываем, только когда заявок накопилось достаточно (порог в шаблоне),
        # чтобы рядом с «30 мастеров» не красовалась унылая «3 заявки».
        'done_leads': Lead.objects.filter(status='done').count(),
    }
    return render(request, 'news/home.html', context)


def article_list(request):
    """Список опубликованных статей с поиском и фильтрами."""
    qs = Article.objects.filter(is_published=True).select_related('city', 'service')

    query = request.GET.get('q', '').strip()
    if query:
        qs = qs.filter(
            Q(title__icontains=query)
            | Q(short_description__icontains=query)
            | Q(content__icontains=query)
        )

    rubric = request.GET.get('rubric', '')
    if rubric:
        qs = qs.filter(rubric=rubric)

    city_id = request.GET.get('city')
    if city_id:
        qs = qs.filter(city_id=city_id)

    context = {
        'articles': qs,
        'rubrics': [{'value': value, 'label': label} for value, label in Service.RUBRIC_CHOICES],
        'rubric': rubric,
        'query': query,
    }
    return render(request, 'news/article_list.html', context)


def article_detail(request, slug):
    """Страница статьи + похожие исполнители по услуге или городу."""
    article = get_object_or_404(Article, slug=slug, is_published=True)

    related = Executor.objects.filter(is_active=True)
    if article.service:
        related = related.filter(services=article.service)
    elif article.city:
        related = related.filter(city=article.city)
    related_executors = related.distinct()[:4]

    return render(request, 'news/article_detail.html', {
        'article': article,
        'related_executors': related_executors,
    })


def executor_list(request):
    """Анкеты исполнителей с фильтрами по городу и услуге."""
    executors = Executor.objects.filter(is_active=True).prefetch_related('services').select_related('city')

    city_id = request.GET.get('city')
    current_city = None
    if city_id:
        current_city = City.objects.filter(pk=city_id).first()
        if current_city:
            executors = executors.filter(city=current_city)

    service_id = request.GET.get('service')
    current_service = None
    if service_id:
        current_service = Service.objects.filter(pk=service_id).first()
        if current_service:
            executors = executors.filter(services=current_service).distinct()

    return render(request, 'news/executor_list.html', {
        'executors': executors,
        'current_city': current_city,
        'current_service': current_service,
    })


@rate_limit('lead', limit=5, per=3600)
def executor_detail(request, slug):
    """Анкета исполнителя + форма заявки."""
    executor = get_object_or_404(Executor, slug=slug, is_active=True)

    if request.method == 'POST':
        if request.POST.get('website'):
            # Заполнил honeypot — бот; молча возвращаем на страницу анкеты
            return redirect('news:executor_detail', slug=executor.slug)
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.executor = executor
            if request.user.is_authenticated:
                lead.owner = request.user
            lead.save()
            executor_user = getattr(executor, 'user', None)
            if executor_user is not None:
                Notification.objects.create(
                    kind=Notification.KIND_LEAD,
                    recipient=executor_user,
                    lead=lead,
                )
            return redirect('news:executor_detail', slug=executor.slug)
    else:
        form = LeadForm()

    return render(request, 'news/executor_detail.html', {'executor': executor, 'form': form})


def stats(request):
    """Статистика: всего статей, разбивка по городам и услугам."""
    total = Article.objects.filter(is_published=True).count()
    by_city = (
        City.objects
        .annotate(num_articles=Count('articles', filter=Q(articles__is_published=True)))
        .filter(num_articles__gt=0)
    )
    by_service = (
        Service.objects
        .annotate(num_articles=Count('articles', filter=Q(articles__is_published=True)))
        .filter(num_articles__gt=0)
    )
    return render(request, 'news/stats.html', {
        'total': total,
        'by_city': by_city,
        'by_service': by_service,
    })


@login_required
def executor_leads(request):
    """Заявки на анкету текущего исполнителя."""
    executor = getattr(request.user, 'executor', None)
    leads = executor.leads.all() if executor else Lead.objects.none()
    return render(request, 'news/executor_leads.html', {'executor': executor, 'leads': leads})


@login_required
def lead_done(request, pk):
    """Отметить заявку обработанной (только для своего исполнителя)."""
    executor = getattr(request.user, 'executor', None)
    lead = get_object_or_404(Lead, pk=pk)
    if executor and lead.executor_id == executor.pk:
        lead.status = 'done'
        lead.save()
    return redirect('news:executor_leads')


@login_required
def my_leads(request):
    """Заявки, оставленные текущим пользователем."""
    leads = request.user.leads.select_related('executor')
    return render(request, 'news/my_leads.html', {'leads': leads})


def register(request):
    """Регистрация живёт в приложении accounts — просто отправляем туда."""
    return redirect('register')


def robots(request):
    return render(request, 'robots.txt', content_type='text/plain')




from django.contrib.auth.decorators import login_required  # noqa
from django.shortcuts import get_object_or_404, redirect, render  # noqa


@login_required
def executor_edit(request):
    """Редактирование анкеты мастера — только её владельцем."""
    executor = getattr(request.user, 'executor', None)
    if executor is None:
        return redirect('news:home')
    if request.method == 'POST':
        form = ExecutorProfileForm(request.POST, request.FILES, instance=executor)
        if form.is_valid():
            form.save()
            return redirect('news:executor_detail', slug=executor.slug)
    else:
        form = ExecutorProfileForm(instance=executor)
    return render(request, 'news/executor_edit.html', {'form': form, 'executor': executor})
