import re

NON_DIGIT = re.compile(r'\D')


def digits_only(value):
    """Только цифры: '+7 (918) 123-45-67' -> '79181234567'."""
    return NON_DIGIT.sub('', str(value or ''))


def normalize_phone(value):
    """Нормализация в базу: 8/9/без кода -> 11 цифр с ведущей 7."""
    d = digits_only(value)
    if not d:
        return ''
    if len(d) == 10 and d[0] in '34569':
        d = '7' + d
    elif len(d) == 11 and d[0] == '8':
        d = '7' + d[1:]
    if len(d) == 11 and d[0] == '7':
        return d
    return ''


def fmt_phone(value):
    """Для показа: '79181234567' -> '+7 (918) 123-45-67'."""
    d = digits_only(value)
    if len(d) == 11 and d[0] == '8':
        d = '7' + d[1:]
    if len(d) == 11 and d[0] == '7':
        return '+7 ({}) {}-{}-{}'.format(d[1:4], d[4:7], d[7:9], d[9:11])
    return value or ''
