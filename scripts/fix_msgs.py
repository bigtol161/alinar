import pathlib

p = pathlib.Path('news/views.py')
s = p.read_text()

old_line = "            messages.error(request, 'Проверьте заполнение полей: имя и телефон обязательны.')\n"
if old_line in s:
    s = s.replace(old_line, '', 1)
    p.write_text(s)
    print('Дублирующий баннер убран')
else:
    print('Строка не найдена — пришли: sed -n "124,134p" news/views.py')
