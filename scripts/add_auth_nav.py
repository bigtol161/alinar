import pathlib

p = pathlib.Path('news/templates/base.html')
s = p.read_text()

anchor = """      {% if user.is_authenticated %}
        <a href="{% url 'news:my_leads' %}" class="text-decoration-none text-body">Мои заявки</a>
      {% endif %}"""

addition = anchor + """
      {% if user.is_authenticated %}
        <span class="text-body">Привет, {{ user.username }}</span>
        <form method="post" action="{% url 'news:logout' %}" class="d-inline">
          {% csrf_token %}
          <button type="submit" class="btn btn-link btn-sm text-decoration-none text-body p-0 align-baseline">Выйти</button>
        </form>
      {% else %}
        <a href="{% url 'login' %}" class="text-decoration-none text-body">Войти</a>
      {% endif %}"""

if 'Привет, {{ user.username }}' in s:
    print('Блок уже добавлен')
else:
    n = s.count(anchor)
    if n >= 2:
        s = s.replace(anchor, addition)
        p.write_text(s)
        print(f'Блок добавлен, вхождений: {n}')
    else:
        print('Якорь не совпал — пришли: sed -n "20,55p" news/templates/base.html')
