import pathlib

p = pathlib.Path('news/templates/news/executor_list.html')
h = p.read_text()

# 1. Динамический заголовок + чипы фильтров
old_header = """<div class="d-flex justify-content-between align-items-center mb-3">
  <h1 class="h3 mb-0">Исполнители в Ростове-на-Дону</h1>
  <span class="ya-muted">Всего: {{ executors|length }}</span>
</div>"""
new_header = """<div class="d-flex justify-content-between align-items-center mb-3">
  <h1 class="h3 mb-0">Исполнители{% if current_city %} в {{ current_city.name }}{% endif %}</h1>
  <span class="ya-muted">Всего: {{ executors|length }}</span>
</div>

{% if current_service or current_city %}
<div class="mb-3 d-flex gap-2 align-items-center flex-wrap">
  <span class="ya-muted small">Фильтры:</span>
  {% if current_city %}
    <a href="{% url 'news:executor_list' %}{% if current_service %}?service={{ current_service.pk }}{% endif %}"
       class="ya-chip text-decoration-none">{{ current_city.name }} ✕</a>
  {% endif %}
  {% if current_service %}
    <a href="{% url 'news:executor_list' %}{% if current_city %}?city={{ current_city.pk }}{% endif %}"
       class="ya-chip text-decoration-none">{{ current_service.name }} ✕</a>
  {% endif %}
  <a href="{% url 'news:executor_list' %}" class="small text-decoration-none">сбросить всё</a>
</div>
{% endif %}"""

if 'Фильтры:' in h:
    print('1: чипы уже есть')
elif old_header in h:
    h = h.replace(old_header, new_header)
    print('1: заголовок и чипы добавлены')
else:
    print('1: якорь шапки не совпал')

# 2. Теги услуг в карточке — после чипа специальности
old_spec = """        {% if executor.specialty %}
          <span class="ya-chip mb-1 align-self-start">{{ executor.specialty }}</span>
        {% endif %}"""
new_spec = old_spec + """
        {% if executor.services.all %}
          <div class="mb-2">
            {% for s in executor.services.all|slice:":4" %}
              <span class="ya-chip me-1">{{ s.name }}</span>
            {% endfor %}
          </div>
        {% endif %}"""

if 'executor.services.all|slice' in h:
    print('2: теги услуг уже есть')
elif old_spec in h:
    h = h.replace(old_spec, new_spec)
    print('2: теги услуг добавлены')
else:
    print('2: якорь карточки не совпал')

# 3. Осмысленное пустое состояние при активных фильтрах
old_empty = """  {% empty %}
  <div class="col-12"><p class="ya-muted">Анкет пока нет — добавьте первую в админке.</p></div>"""
new_empty = """  {% empty %}
  <div class="col-12">
    {% if current_service or current_city %}
      <p class="ya-muted">По выбранным фильтрам ничего не нашлось.
        <a href="{% url 'news:executor_list' %}" class="text-decoration-none">Сбросить фильтры</a></p>
    {% else %}
      <p class="ya-muted">Анкет пока нет — добавьте первую в админке.</p>
    {% endif %}
  </div>"""

if 'По выбранным фильтрам' in h:
    print('3: пустое состояние уже обновлено')
elif old_empty in h:
    h = h.replace(old_empty, new_empty)
    print('3: пустое состояние обновлено')
else:
    print('3: якорь empty не совпал')

p.write_text(h)
