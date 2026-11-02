# Генератор карты проекта: собирает классы, функции и маршруты
# в docs/STRUCTURE.md. Запуск: python docs/build_map.py
import ast, os, datetime

out = ['# Карта проекта (автогенерация)', '',
       f'Обновлено: {datetime.date.today().strftime("%d.%m.%Y")}',
       '',
       'Этот файл создаётся скриптом docs/build_map.py — вручную не править, '
       'изменения затрутся при следующем запуске.', '']

def first_line(obj):
    doc = ast.get_docstring(obj)
    return f' — {doc.splitlines()[0]}' if doc else ''

for app in ('accounts', 'news'):
    out.append(f'## Приложение {app}/')
    for fname in sorted(os.listdir(app)):
        if not fname.endswith('.py'):
            continue
        path = os.path.join(app, fname)
        out.append(f'### {fname}')
        for node in ast.parse(open(path, encoding='utf-8').read()).body:
            if isinstance(node, ast.ClassDef):
                out.append(f'- **класс {node.name}**{first_line(node)}')
                for sub in node.body:
                    if isinstance(sub, ast.FunctionDef) and not sub.name.startswith('__'):
                        out.append(f'  - метод `{sub.name}`{first_line(sub)}')
            elif isinstance(node, ast.FunctionDef):
                out.append(f'- **функция `{node.name}`**{first_line(node)}')
        out.append('')

# Маршруты из news/urls.py — разбор обычными строковыми методами
out.append('## Маршруты news/')
urls_text = open('news/urls.py', encoding='utf-8').read()
for line in urls_text.splitlines():
    line = line.strip()
    if not line.startswith('path('):
        continue
    q1 = line.find("'")
    q2 = line.find("'", q1 + 1)
    route = line[q1 + 1:q2] if q1 != -1 and q2 != -1 else '?'
    name = 'без имени'
    name_pos = line.find("name='")
    if name_pos != -1:
        end = line.find("'", name_pos + 6)
        name = line[name_pos + 6:end]
    out.append(f'- `{route}` → имя `{name}`')

open('docs/STRUCTURE.md', 'w', encoding='utf-8').write('\n'.join(out))
print('Создан docs/STRUCTURE.md')
