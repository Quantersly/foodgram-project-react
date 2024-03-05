from django.db import models
from django.db.models import UniqueConstraint


class Ingredient(models.Model):
    """Модель Ингридиента"""

    name = models.CharField(
        'Название',
        max_length=200,
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200,
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        constraints = (
            UniqueConstraint(
                fields=(
                    'name',
                    'measurement_unit',
                ),
                name='unique_ingredient'
            ),
        )
        ordering = ('pk',)

    def __str__(self):
        """Строковое представление модели"""

        return self.name
