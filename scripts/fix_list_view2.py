import pathlib

p = pathlib.Path('news/views.py')
s = p.read_text()

old_block = """    if rubric and rubric in Article.Rubric.values:
        articles = articles.filter(rubric=rubric)
    rubrics = [
        {'value': value, 'label': label}
        for value, label in Article.Rubric.choices
    ]"""

new_block = """    rubric_field = Article._meta.get_field('rubric')
    rubric_values = {value for value, label in rubric_field.choices}
    if rubric and rubric in rubric_values:
        articles = articles.filter(rubric=rubric)
    rubrics = [
        {'value': value, 'label': label}
        for value, label in rubric_field.choices
    ]"""

if "get_field('rubric')" in s:
    print('Правка уже есть')
elif old_block in s:
    s = s.replace(old_block, new_block, 1)
    p.write_text(s)
    print('Вьюха исправлена: choices берутся из поля модели')
else:
    print('Блок не найден — пришли: sed -n "22,45p" news/views.py')
