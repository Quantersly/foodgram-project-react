from django.db import models

from .model_user import User


class Follow(models.Model):
    """Модель Подписки"""

    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписики'
        ordering = ('-pk',)
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'author',
                ],
                name='unique_follow',
            )
        ]

    def __str__(self):
        """Строковое представление модели"""

        return f'{self.user} {self.author}'
