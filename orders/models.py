from django.conf import settings
from django.db import models

from core.models import City, Service
from news.models import Executor
from core.phones import digits_only


class Order(models.Model):
    """Заказ от заказчика: что нужно сделать, где и за сколько."""

    STATUS_CHOICES = (
        ('new', 'Открыт'),
        ('closed', 'Закрыт'),
    )

    title = models.CharField('Что нужно сделать', max_length=200)
    description = models.TextField('Подробности')
    city = models.ForeignKey(
        City,
        verbose_name='Город',
        on_delete=models.CASCADE,
        related_name='orders',
    )
    service = models.ForeignKey(
        Service,
        verbose_name='Услуга',
        on_delete=models.CASCADE,
        related_name='orders',
    )
    budget = models.DecimalField(
        'Бюджет, руб.',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Можно не указывать — тогда мастер предложит цену сам',
    )
    contact_name = models.CharField('Как к вам обращаться', max_length=100)
    phone = models.CharField('Телефон', max_length=32)
    number = models.CharField('Номер заявки', max_length=16, unique=True, blank=True, editable=False)
    status = models.CharField('Статус', max_length=16, choices=STATUS_CHOICES, default='new')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Заказчик',
        on_delete=models.CASCADE,
        related_name='orders',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    def save(self, *args, **kwargs):
        self.phone = digits_only(self.phone)
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and not self.number:
            self.number = 'DS-{:02d}-{:05d}'.format(self.created_at.year % 100, self.pk)
            super().save(update_fields=['number'])

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.title


class Response(models.Model):
    """Отклик мастера на заказ."""

    order = models.ForeignKey(
        Order,
        verbose_name='Заказ',
        on_delete=models.CASCADE,
        related_name='responses',
    )
    executor = models.ForeignKey(
        Executor,
        verbose_name='Мастер',
        on_delete=models.CASCADE,
        related_name='order_responses',
    )
    message = models.TextField('Сообщение заказчику', blank=True)
    price = models.DecimalField(
        'Предлагаемая цена, руб.',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Можно не указывать — обсудим по телефону',
    )
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        constraints = (
            models.UniqueConstraint(
                fields=('order', 'executor'),
                name='unique_response_per_order',
            ),
        )
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'

    def __str__(self):
        return f'{self.executor.name} → {self.order.title}'
