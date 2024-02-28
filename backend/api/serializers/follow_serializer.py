from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .list_of_following_recipes_serializer import ListOfFollowingRecipesSerializer
from users.models import User


class FollowSerializer(UserSerializer):
    """Сериализатор подписoк"""

    recipes_count = serializers.IntegerField(
        source='recipes.count',
        read_only=True,
    )
    recipes = SerializerMethodField(method_name='get_recipes')
    is_subscribed = serializers.BooleanField(default=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'recipes_count',
            'recipes',
            'is_subscribed',
        )
        read_only_fields = (
            'email',
            'username',
            'first_name',
            'last_name',
        )

    def get_recipes(self, obj):
        """Метод получения рецептов"""

        recipes = obj.recipes.all()
        serializer = ListOfFollowingRecipesSerializer(
            recipes,
            many=True,
            context=self.context,
        )
        return serializer.data
