import pathlib

p = pathlib.Path('news/views.py')
s = p.read_text()

# Пустой else: после if form.is_valid() — убираем его целиком
broken = "            form = LeadForm()\n        else:\n    else:\n"
fixed = "            form = LeadForm()\n    else:\n"

if broken in s:
    s = s.replace(broken, fixed, 1)
    p.write_text(s)
    print('Пустой else убран, блок цел')
else:
    print('Шаблон не совпал — пришли: sed -n "120,142p" news/views.py')
