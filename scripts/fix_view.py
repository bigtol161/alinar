import pathlib

p = pathlib.Path('news/views.py')
s = p.read_text()

old_block = """    related_executors = []
    if article.service:
        related_executors = (
            Executor.objects.filter(is_active=True, services=article.service)
            .select_related('city')
            .prefetch_related('services')
        )
    return render(request, 'news/article_detail.html', {"""

new_block = """    related_executors = []
    if article.service:
        related_executors = list(
            Executor.objects.filter(is_active=True, services=article.service)
            .select_related('city')
            .prefetch_related('services')
        )
    if article.rubric and article.rubric != 'other':
        seen = {e.pk for e in related_executors}
        rubric_executors = (
            Executor.objects.filter(is_active=True, services__rubric=article.rubric)
            .exclude(pk__in=seen)
            .select_related('city')
            .prefetch_related('services')
        )
        related_executors += list(rubric_executors)
    return render(request, 'news/article_detail.html', {"""

if 'services__rubric' in s:
    print('Правка уже есть')
elif old_block in s:
    s = s.replace(old_block, new_block, 1)
    p.write_text(s)
    print('Вьюха article_detail обновлена')
else:
    print('Блок не найден — пришли вывод: sed -n "35,55p" news/views.py')
