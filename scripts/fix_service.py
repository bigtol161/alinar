import pathlib

p = pathlib.Path('core/models.py')
s = p.read_text()

if 'rubric' in s:
    print('Правка уже есть')
else:
    s = s.replace(
        "    name = models.CharField('Название услуги', max_length=200)",
        """    name = models.CharField('Название услуги', max_length=200)
    RUBRIC_CHOICES = (
        ('repair', 'Ремонт'),
        ('plumbing', 'Сантехника'),
        ('electrics', 'Электрика'),
        ('cleaning', 'Уборка'),
        ('moving', 'Переезды и грузчики'),
        ('beauty', 'Красота и здоровье'),
        ('other', 'Другое'),
    )
    rubric = models.CharField(
        'Рубрика',
        max_length=20,
        choices=RUBRIC_CHOICES,
        default='other',
    )""",
        1,
    )
    p.write_text(s)
    print('Поле rubric добавлено')
