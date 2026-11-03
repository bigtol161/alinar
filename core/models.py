from django.db import models

# Create your models here.
from django.db import models


class City(models.Model):
    name = models.CharField('Название города', max_length=100)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField('Название услуги', max_length=200)
    RUBRIC_CHOICES = (
        ('repair', 'Ремонт'),
        ('plumbing', 'Сантехника'),
        ('electrics', 'Электрика'),
        ('cleaning', 'Уборка'),
        ('moving', 'Переезды и грузчики'),
        ('beauty', 'Красота и здоровье'),
        ('climate', 'Климат и кондиционеры'),
        ('appliances', 'Ремонт бытовой техники'),
        ('handyman', 'Муж на час'),
        ('furniture', 'Сборка мебели'),
        ('windows', 'Окна и остекление'),
        ('pests', 'Дезинсекция и дезинфекция'),
        ('other', 'Другое'),
    )
    rubric = models.CharField(
        'Рубрика',
        max_length=20,
        choices=RUBRIC_CHOICES,
        default='other',
    )

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name
