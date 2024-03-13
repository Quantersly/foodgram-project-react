from django.contrib.auth import get_user_model
from django_filters import rest_framework
from rest_framework import exceptions

from recipes.models import (
    Recipe,
    Tag,
)

User = get_user_model()


class RecipeFilter(rest_framework.FilterSet):
    """Фильтр рецептов"""

    author = rest_framework.ModelChoiceFilter(queryset=User.objects.all())
    tags = rest_framework.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_favorited = rest_framework.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = rest_framework.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = (
            'author',
            'tags',
            'is_favorited',
            'is_in_shopping_cart',
        )

    def filter_is_favorited(self, queryset, name, value):
        """Фильтр проверки рецепта на наличие избранном """

        if not self.request.user.is_authenticated:
            return []
        if value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        """Фильтр проверки рецепта на наличие покупах"""

        if not self.request.user.is_authenticated:
            raise exceptions.AuthenticationFailed('Требуеся автроризоваться')
        if value:
            return queryset.filter(shopping__user=self.request.user)
        return queryset
