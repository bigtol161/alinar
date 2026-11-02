import pathlib

p = pathlib.Path('news/templates/news/executor_detail.html')
s = p.read_text()

old_block = """      <form method="post" novalidate>
        {% csrf_token %}
        <div class="row g-2">
          <div class="col-md-5">{{ form.name }}</div>
          <div class="col-md-4">{{ form.phone }}</div>
          <div class="col-md-3">
            <button type="submit" class="ya-btn w-100">Отправить заявку</button>
          </div>
        </div>
        <div class="mt-2">{{ form.message }}</div>
      </form>"""

new_block = """      <form method="post" novalidate>
        {% csrf_token %}
        {% if form.errors %}
          <div class="text-danger small mb-2">
            {% for field in form %}
              {% for error in field.errors %}<div>{{ error }}</div>{% endfor %}
            {% endfor %}
            {% for error in form.non_field_errors %}<div>{{ error }}</div>{% endfor %}
          </div>
        {% endif %}
        <div class="row g-2">
          <div class="col-md-5">{{ form.name }}</div>
          <div class="col-md-4">{{ form.phone }}</div>
          <div class="col-12 mt-2">{{ form.message }}</div>
          <div class="col-md-3">
            <button type="submit" class="ya-btn w-100">Отправить заявку</button>
          </div>
        </div>
      </form>"""

if 'form.errors' in s:
    print('Правка уже есть')
elif old_block in s:
    s = s.replace(old_block, new_block, 1)
    p.write_text(s)
    print('Форма заявки обновлена')
else:
    print('Блок не найден — проверь пробелы в executor_detail.html')
