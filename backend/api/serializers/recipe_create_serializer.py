from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from recipes.models import (
    Recipe,
    RecipeIngredients,
    Tag,
)
from .ingredient_in_recipe_serializer import (
    IngredientInRecipeSerializer
)
from .recipe_read_serializer import (
    RecipeReadSerializer
)


class RecipeCreateSerializer(ModelSerializer):
    """Сериализатор создания рецепта"""

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    author = UserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def validate_tags(self, value):
        """Метод валидации тегов"""

        if not value:
            raise ValidationError(
                'Добавление тега рецепту обязательно'
            )
        return value

    def validate_ingredients(self, value):
        """Метод валидации ингредиентов"""

        if not value:
            raise ValidationError(
                'Добавление ингредиента в рецепт обязательно'
            )
        for i in value:
            if i['amount'] <= 0:
                raise ValidationError(
                    'Колличество ингредиента должно быть больше 0'
                )
        return value

    def to_representation(self, instance):
        """Метод репрезентации рецепта при его создании"""

        request = self.context.get('request')
        context = {'request': request}
        return RecipeReadSerializer(
            instance,
            context=context,
        ).data

    def create(self, validated_data):
        """Метод создания рецепта"""

        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            RecipeIngredients.objects.create(
                recipe=recipe,
                ingredient=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )
        return recipe

    def update(self, instance, validated_data):
        """Метод редактирования рецепта"""

        tags = validated_data.pop(
            'tags',
            None,
        )
        if tags is not None:
            instance.tags.set(tags)
        ingredients = validated_data.pop(
            'ingredients',
            None,
        )
        if ingredients is not None:
            instance.ingredients.clear()
            for ingredient in ingredients:
                amount = ingredient['amount']
                RecipeIngredients.objects.update_or_create(
                    recipe=instance,
                    ingredient=ingredient.get('id'),
                    defaults={'amount': amount},
                )
        return super().update(
            instance,
            validated_data,
        )
