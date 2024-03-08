from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)
from django.db import models

from recipes.models import (
    Ingredient,
    Recipe,
)


class RecipeIngredients(models.Model):
    """Модель Ингридиентов В Рецепте"""

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='recipeingredients',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингридиент',
        on_delete=models.CASCADE,
        related_name='recipeingredients',
    )
    amount = models.PositiveSmallIntegerField(
        'Колличество',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(32767),
        ),
    )

    class Meta:
        verbose_name = 'ингридиент для рецепта'
        verbose_name_plural = 'ингридиенты для рецепта'

    def __str__(self):
        """Строковое представление модели"""

        return f'{str(self.ingredient)} in {str(self.recipe)}-{self.amount}'
