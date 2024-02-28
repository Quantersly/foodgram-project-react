from django.db import models
from django.db.models import UniqueConstraint

from users.models import User
from .model_recipe import Recipe


class ShoppingCart(models.Model):
    """Модель Списка Покупок"""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shopping',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='shopping',
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Список Покупок'
        constraints = (
            UniqueConstraint(
                fields=(
                    'user',
                    'recipe',
                ),
                name='unique_shopping_cart'
            ),
        )

    def __str__(self):
        """Строковое представление модели"""
        
        return f'Рецепт, {self.recipe}, добавлен в корзину'
