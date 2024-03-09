from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)
from django.db import models
from django.db.models import UniqueConstraint

from api.validators import validate_year
from users.models import User
from recipes.models import (
    Ingredient,
    Tag,
)


class Recipe(models.Model):
    """Модель Рецепта"""

    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    name = models.CharField(
        'Название',
        max_length=200,
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/',
    )
    text = models.TextField(
        verbose_name='Текст',
        unique=True,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингридиенты',
        through='RecipeIngredients',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        related_name='recipes',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=(
            MinValueValidator(
                1,
                message='Наименьшее значение времени приготовления - 1',
            ),
            MaxValueValidator(
                32267,
                message='Наибольшее значение времени приготовления - 44640',
            )
        ),
    )
    created = models.DateTimeField(
        'Дата публикации',
        validators=(validate_year,),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = (
            UniqueConstraint(
                fields=(
                    'author',
                    'name',
                    'text',
                    'cooking_time',
                ),
                name='unique_recipe'
            ),
        )
        ordering = ('-created',)

    def __str__(self):
        """Строковое представление модели"""

        return self.name
