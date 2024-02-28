from django.db import models


class Tag(models.Model):
    """Модель тега"""

    name = models.CharField(
        verbose_name='Имя тега',
        max_length=200,
        unique=True,
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        """Строковое представление модели"""
        
        return self.name
