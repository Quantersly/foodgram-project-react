from djoser.serializers import UserSerializer
from rest_framework.fields import SerializerMethodField

from users.models import Follow, User


class UserSerializer(UserSerializer):
    """Сериализатор пользователя"""

    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        """Метод проверки подписки пользователя"""

        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=user,
            author=obj,
        ).exists()
