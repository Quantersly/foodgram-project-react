from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from recipes.models import (
    Ingredient,
    RecipeIngredients,
)


class IngredientInRecipeSerializer(ModelSerializer):
    """
    Сериализатор для отоброжения ингридиента в рецепте при
    его создании
    """

    id = PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredients
        fields = (
            'id',
            'amount',
            'name',
            'measurement_unit',
        )

    def to_representation(self, instance):
        """Метод репрезентации ингредиента в создании рецепта"""

        data = super().to_representation(instance)
        data['id'] = instance.ingredient.id
        return data

    def validate_amount(self, value):
        """Метод валидации количества ингредиентов"""

        if value <= 0:
            raise ValidationError(
                'Убедитесь, что это значение больше либо равно 1.'
            )
        return value
