from django.db import models

# Create your models here.
from django.db import models
from django.utils.text import slugify


class Article(models.Model):
    RUBRIC_CHOICES = (
        ('repair', 'Ремонт'),
        ('plumbing', 'Сантехника'),
        ('electrics', 'Электрика'),
        ('cleaning', 'Уборка'),
        ('moving', 'Переезды и грузчики'),
        ('beauty', 'Красота и здоровье'),
        ('other', 'Другое'),
    )

    title = models.CharField('Заголовок', max_length=200)
    slug = models.SlugField('Адрес страницы', max_length=220, unique=True)
    rubric = models.CharField('Рубрика', max_length=20, choices=RUBRIC_CHOICES, default='other')
    city = models.ForeignKey(
        'core.City',
        verbose_name='Город',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='articles',
    )
    service = models.ForeignKey(
        'core.Service',
        verbose_name='Услуга',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='articles',
    )
    short_description = models.TextField('Краткое описание', blank=True)
    content = models.TextField('Текст статьи')
    cover = models.ImageField('Обложка', upload_to='news/', blank=True, null=True)
    meta_title = models.CharField('SEO заголовок', max_length=200, blank=True)
    meta_description = models.TextField('SEO описание', blank=True)
    is_published = models.BooleanField('Опубликовано', default=False)
    published_at = models.DateTimeField('Дата публикации', null=True, blank=True)
    created_at = models.DateTimeField('Создана', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлена', auto_now=True)

    class Meta:
        ordering = ('-published_at', '-created_at')
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)[:220]
        super().save(*args, **kwargs)


from core.models import City, Service


class Executor(models.Model):
    name = models.CharField('Имя или название организации', max_length=150)
    slug = models.SlugField('Слаг (для адреса страницы)', max_length=150, unique=True)
    city = models.ForeignKey(
        City,
        verbose_name='Город',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='executors',
    )
    services = models.ManyToManyField(
        Service,
        verbose_name='Услуги',
        blank=True,
        related_name='executors',
    )
    user = models.OneToOneField(
        'auth.User',
        verbose_name='Аккаунт исполнителя',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='executor',
    )
    phone = models.CharField('Телефон', max_length=30, blank=True)
    description = models.TextField('Описание', blank=True)
    photo = models.ImageField('Фото', upload_to='executors/', blank=True, null=True)
    specialty = models.CharField('Специальность', max_length=100, blank=True, help_text='Например: сантехник, электрик')
    price_from = models.PositiveIntegerField('Цена от, руб.', null=True, blank=True)
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField('Добавлен', auto_now_add=True)

    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'
        ordering = ['name']

    def __str__(self):
        return self.name



class Lead(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новая'),
        ('done', 'Обработана'),
    )

    executor = models.ForeignKey(
        Executor,
        verbose_name='Мастер',
        on_delete=models.CASCADE,
        related_name='leads',
    )
    owner = models.ForeignKey(
        'auth.User',
        verbose_name='Аккаунт заказчика',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='leads',
    )
    name = models.CharField('Имя', max_length=100)
    phone = models.CharField('Телефон', max_length=30)
    message = models.TextField('Что нужно сделать', blank=True)
    status = models.CharField('Статус', max_length=10, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField('Создана', auto_now_add=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.name} — {self.executor.name}'
