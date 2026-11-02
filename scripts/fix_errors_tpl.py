import pathlib

p = pathlib.Path('news/templates/news/executor_detail.html')
s = p.read_text()

old_block = """        {% if form.errors %}
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
        </div>"""

new_block = """        <div class="row g-2">
          <div class="col-md-5">
            {{ form.name }}
            {% for error in form.name.errors %}<div class="text-danger small">{{ error }}</div>{% endfor %}
          </div>
          <div class="col-md-4">
            {{ form.phone }}
            {% for error in form.phone.errors %}<div class="text-danger small">{{ error }}</div>{% endfor %}
          </div>
          <div class="col-12 mt-2">
            {{ form.message }}
            {% for error in form.message.errors %}<div class="text-danger small">{{ error }}</div>{% endfor %}
          </div>
          <div class="col-md-3">
            <button type="submit" class="ya-btn w-100">Отправить заявку</button>
          </div>
        </div>"""

if old_block in s:
    s = s.replace(old_block, new_block, 1)
    p.write_text(s)
    print('Ошибки теперь привязаны к своим полям')
else:
    print('Блок не совпал — пришли: cat news/templates/news/executor_detail.html | sed -n "55,85p"')
