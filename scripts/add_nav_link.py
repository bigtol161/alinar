import pathlib

p = pathlib.Path('news/templates/base.html')
s = p.read_text()

anchor = """<a href="{% url 'news:executor_list' %}" class="text-decoration-none text-body">Исполнители</a>"""
addition = anchor + """
      {% if user.is_authenticated %}
        <a href="{% url 'news:my_leads' %}" class="text-decoration-none text-body">Мои заявки</a>
      {% endif %}"""

if 'my_leads' in s:
    print('Ссылка уже есть')
elif anchor in s:
    s = s.replace(anchor, addition)
    p.write_text(s)
    print('Ссылка добавлена в шапку')
else:
    print('Не нашёл якорь — пришли: sed -n "20,50p" news/templates/base.html')
