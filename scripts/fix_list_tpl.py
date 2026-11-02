import pathlib

p = pathlib.Path('news/templates/news/article_list.html')
s = p.read_text()

old_block = """{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
  <h1 class="h3 mb-0">Статьи</h1>
  <span class="ya-muted">Всего: {{ articles|length }}</span>
</div>
"""

new_block = """{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
  <h1 class="h3 mb-0">Статьи</h1>
  <span class="ya-muted">Всего: {{ articles|length }}</span>
</div>

<div class="mb-4 d-flex flex-wrap gap-2">
  <a href="?{% if query %}q={{ query|urlencode }}{% endif %}"
     class="ya-chip {% if not rubric %}ya-chip-active{% endif %} text-decoration-none">Все</a>
  {% for r in rubrics %}
    <a href="?{% if query %}q={{ query|urlencode }}&amp;{% endif %}rubric={{ r.value }}"
       class="ya-chip {% if rubric == r.value %}ya-chip-active{% endif %} text-decoration-none">{{ r.label }}</a>
  {% endfor %}
</div>
"""

s = s.replace(old_block, new_block, 1)
s = s.replace('article.category', 'article.get_rubric_display', 1)
p.write_text(s)
print('Шаблон article_list обновлён')
