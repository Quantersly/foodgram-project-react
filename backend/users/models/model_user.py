from django.contrib.auth.models import AbstractUser
from django.db import models

from ..validators import validate_username


class User(AbstractUser):
    """Модель Пользователя"""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name'
    ]

    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        validators=[
            validate_username,
        ],
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
    )
    password = models.CharField(
        max_length=150,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('pk',)
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'email',
                    'username',
                ),
                name='unique_auth',
            ),
        )

    def __str__(self):
        """Строковое представление модели"""

        return self.username
