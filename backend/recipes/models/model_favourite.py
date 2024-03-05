from django.db import models
from django.db.models import UniqueConstraint

from users.models import User
from recipes.models import Recipe


class Favourite(models.Model):
    """Модель Избранного"""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='favorites',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = (
            UniqueConstraint(
                fields=(
                    'user',
                    'recipe',
                ),
                name='unique_favourite',
            ),
        )

    def __str__(self):
        """Строковое представление модели"""

        return f'Рецепт, {self.recipe}, добавлен в избранное'
