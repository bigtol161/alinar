from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_CHOICES = (
        ('customer', 'Заказчик'),
        ('contractor', 'Исполнитель'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField('Роль', max_length=20, choices=ROLE_CHOICES, default='customer')
    bio = models.TextField('О себе', blank=True)
    city = models.CharField('Город', max_length=100, blank=True)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    avatar = models.ImageField('Аватар', upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} ({self.get_role_display()})'
