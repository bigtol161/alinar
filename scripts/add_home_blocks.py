import pathlib

# --- views.py ---
v = pathlib.Path('news/views.py')
s = v.read_text()

s = s.replace(
    "from .models import Article, Lead",
    "from .models import Article, Executor, Lead",
)

old = """    cities = City.objects.annotate(
        num_articles=Count('articles', filter=Q(articles__is_published=True))
    ).filter(num_articles__gt=0).order_by('name')
    return render(request, 'news/home.html', {
        'articles': articles,
        'total': total,
        'cities': cities,
    })"""
new = """    cities = City.objects.annotate(
        num_articles=Count('articles', filter=Q(articles__is_published=True)),
        num_executors=Count('executors', filter=Q(executors__is_active=True)),
    ).filter(num_articles__gt=0).order_by('name')
    popular_services = list(
        Service.objects
        .annotate(num_executors=Count('executors', filter=Q(executors__is_active=True)))
        .filter(num_executors__gt=0)
        .order_by('-num_executors')
    )[:8]
    return render(request, 'news/home.html', {
        'articles': articles,
        'total': total,
        'cities': cities,
        'popular_services': popular_services,
    })"""

if 'popular_services' in s:
    print('views: уже правлено')
elif old in s:
    s = s.replace(old, new)
    v.write_text(s)
    print('views: home() обновлена')
else:
    print('views: якорь не совпал — пришли: grep -n -A10 "def home" news/views.py')

# --- home.html ---
t = pathlib.Path('news/templates/news/home.html')
h = t.read_text()

# 1. Блок популярных услуг перед городами
services_block = """<!-- Популярные услуги -->
{% if popular_services %}
<section class="mb-4">
  <h2 class="ya-section-title">Популярные услуги</h2>
  <div class="row g-3">
    {% for s in popular_services %}
    <div class="col-6 col-md-3">
      <a href="{% url 'news:executor_list' %}?service={{ s.pk }}" class="ya-tile">
        <span class="fw-bold">{{ s.name }}</span>
        <span class="ya-muted small ms-auto">{{ s.num_executors }} маст.</span>
      </a>
    </div>
    {% endfor %}
  </div>
</section>
{% endif %}

"""
if 'Популярные услуги' in h:
    print('html: услуги уже есть')
elif '<!-- Города: плитки из базы, сами обновляются -->' in h:
    h = h.replace('<!-- Города: плитки из базы, сами обновляются -->',
                  services_block + '<!-- Города: плитки из базы, сами обновляются -->')
    print('html: блок услуг вставлен')
else:
    print('html: якорь городов не найден')

# 2. Счётчики в плитке города
if 'num_executors }} маст.' not in h:
    h = h.replace(
        '<span class="ya-muted small ms-auto">{{ city.num_articles }} шт.</span>',
        '<span class="ya-muted small ms-auto">{{ city.num_articles }} ст. · {{ city.num_executors }} маст.</span>',
    )
    print('html: счётчики городов обновлены')

# 3. Секция городов — скрывать, если пусто
if '{% if cities %}' not in h:
    h = h.replace('<!-- Города: плитки из базы, сами обновляются -->',
                  '{% if cities %}<!-- Города: плитки из базы, сами обновляются -->')
    h = h.replace('\n</section>\n\n<!-- Лента свежих статей -->',
                  '\n</section>\n{% endif %}\n\n<!-- Лента свежих статей -->')
    print('html: пустая секция городов скрыта')

t.write_text(h)
