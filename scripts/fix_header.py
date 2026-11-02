import pathlib

p = pathlib.Path('news/templates/base.html')
s = p.read_text()
changed = False

if 'mobileMenu' not in s:
    old_search = '''    <form action="{% url 'news:article_list' %}" method="get" class="ya-search flex-grow-1">
      <input type="text" name="q" class="form-control"
             placeholder="Статьи, услуги, мастера">
    </form>
    <a href="{% url 'news:register' %}" class="ya-btn text-decoration-none">Стать исполнителем</a>
  </div>
</header>'''
    new_search = '''    <form action="{% url 'news:article_list' %}" method="get" class="ya-search flex-grow-1 d-none d-md-block">
      <input type="text" name="q" class="form-control"
             placeholder="Статьи, услуги, мастера">
    </form>
    <a href="{% url 'news:register' %}" class="ya-btn text-decoration-none">Стать исполнителем</a>
    <button class="ya-burger d-md-none" type="button" data-bs-toggle="collapse" data-bs-target="#mobileMenu" aria-controls="mobileMenu" aria-expanded="false" aria-label="Меню">
      <span></span><span></span><span></span>
    </button>
  </div>
  <div class="collapse" id="mobileMenu">
    <div class="container d-md-none py-2">
      <form action="{% url 'news:article_list' %}" method="get" class="mb-2">
        <input type="text" name="q" class="form-control" placeholder="Статьи, услуги, мастера">
      </form>
      <nav class="d-flex gap-3 pb-1">
        <a href="{% url 'news:article_list' %}" class="text-decoration-none text-body">Статьи</a>
        <a href="{% url 'news:executor_list' %}" class="text-decoration-none text-body">Исполнители</a>
      </nav>
    </div>
  </div>
</header>'''
    if old_search in s:
        s = s.replace(old_search, new_search, 1)
        changed = True
    else:
        print('Блок шапки не найден дословно — пришли вывод: sed -n "20,40p" news/templates/base.html')
else:
    print('Мобильное меню уже есть')

if 'bootstrap.bundle' not in s:
    s = s.replace('</body>', '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>\n</body>', 1)
    changed = True

if changed:
    p.write_text(s)
    print('base.html обновлён')
