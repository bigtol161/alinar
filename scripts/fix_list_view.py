import pathlib

p = pathlib.Path('news/views.py')
s = p.read_text()

old_block = """    articles = Article.objects.filter(is_published=True)
    query = request.GET.get('q', '').strip()
    if query:
        articles = articles.filter(
            models.Q(title__icontains=query) |
            models.Q(short_description__icontains=query) |
            models.Q(content__icontains=query)
        )
    return render(request, 'news/article_list.html', {
        'articles': articles,
        'query': query,
    })"""

new_block = """    articles = Article.objects.filter(is_published=True)
    query = request.GET.get('q', '').strip()
    rubric = request.GET.get('rubric', '').strip()
    if query:
        articles = articles.filter(
            models.Q(title__icontains=query) |
            models.Q(short_description__icontains=query) |
            models.Q(content__icontains=query)
        )
    if rubric and rubric in Article.Rubric.values:
        articles = articles.filter(rubric=rubric)
    rubrics = [
        {'value': value, 'label': label}
        for value, label in Article.Rubric.choices
    ]
    return render(request, 'news/article_list.html', {
        'articles': articles,
        'query': query,
        'rubric': rubric,
        'rubrics': rubrics,
    })"""

if 'rubrics' in s and "Article.Rubric.choices" in s:
    print('Правка уже есть')
elif old_block in s:
    s = s.replace(old_block, new_block, 1)
    p.write_text(s)
    print('Вьюха article_list обновлена')
else:
    print('Блок не найден — пришли: sed -n "22,36p" news/views.py')
