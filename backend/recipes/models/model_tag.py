from django.db import models
from colorfield.fields import ColorField


class Tag(models.Model):
    """Модель тега"""

    name = models.CharField(
        'Имя тега',
        max_length=200,
        unique=True,
    )
    color = ColorField(
        'Цвет',
        default='#FF0000',
        max_length=7,
        unique=True,
    )
    slug = models.SlugField(
        'Слаг',
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        """Строковое представление модели"""

        return self.name
