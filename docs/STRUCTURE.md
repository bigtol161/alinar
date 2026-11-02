# Карта проекта (автогенерация)

Обновлено: 01.11.2026

Этот файл создаётся скриптом docs/build_map.py — вручную не править, изменения затрутся при следующем запуске.

## Приложение accounts/
### __init__.py

### admin.py
- **класс ProfileAdmin**

### apps.py
- **класс AccountsConfig**

### models.py
- **класс Profile**

### tests.py

### views.py

## Приложение news/
### __init__.py

### admin.py
- **класс ArticleAdmin**
- **класс ExecutorAdmin**
- **класс LeadAdmin**

### apps.py
- **класс NewsConfig**

### forms.py
- **класс LeadForm**

### models.py
- **класс Article**
  - метод `save`
- **класс Executor**
- **класс Lead**

### tests.py

### urls.py

### views.py
- **функция `home`** — Стартовая страница: открывает список статей.
- **функция `article_list`** — Главная страница: список статей.
- **функция `article_detail`** — Детальная страница статьи; увеличивает счётчик просмотров.
- **функция `stats`** — Статистика публикаций.
- **функция `executor_list`** — Список анкет исполнителей.
- **функция `executor_detail`** — Анкета мастера и форма заявки на неё.
- **функция `logout_view`** — Выход из аккаунта.
- **класс RegisterForm**
- **функция `register`** — Регистрация нового пользователя с выбором роли.
- **функция `my_leads`** — Кабинет заказчика: его заявки.
- **функция `executor_leads`** — Кабинет исполнителя: заявки на его анкету.
- **функция `mark_lead_done`** — Закрытие заявки: смена статуса на done.

## Маршруты news/
- `` → имя `article_list`
- `stats/` → имя `stats`
- `executors/` → имя `executor_list`
- `executors/<slug:slug>/` → имя `executor_detail`
- `accounts/register/` → имя `register`
- `accounts/logout/` → имя `logout`
- `my-leads/` → имя `my_leads`
- `executor-leads/` → имя `executor_leads`
- `leads/<int:pk>/done/` → имя `lead_done`
- `<slug:slug>/` → имя `article_detail`