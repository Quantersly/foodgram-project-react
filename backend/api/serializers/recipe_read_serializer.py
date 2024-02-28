from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from recipes.models import (
    Favourite,
    Recipe,
    ShoppingCart,
)
from .ingredient_in_recipe_serializer import (
    IngredientInRecipeSerializer
)
from .tag_serializer import TagSerializer

class RecipeReadSerializer(ModelSerializer):
    """Сериализатор получения рецептов"""

    tags = TagSerializer(
        many=True,
        read_only=True,
    )
    author = UserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(
        source='recipeingredients',
        many=True,
    )
    image = Base64ImageField()
    is_favorited = SerializerMethodField(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        """Метод проверки рецепта на наличие в избранном"""

        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Favourite.objects.filter(
            user=user,
            recipe=obj,
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        """Метод проверки рецепта на наличие в покупках"""
        
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=user,
            recipe=obj,
        ).exists()
