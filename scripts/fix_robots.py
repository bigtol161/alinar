import pathlib

p = pathlib.Path('news/templates/robots.txt')
s = p.read_text()
s = s.replace(
    "Sitemap: http://127.0.0.1:8000/sitemap.xml",
    "Sitemap: {{ request.scheme }}://{{ request.get_host }}{% url 'sitemap' %}",
)
p.write_text(s)
print('Sitemap-адрес теперь динамический')
