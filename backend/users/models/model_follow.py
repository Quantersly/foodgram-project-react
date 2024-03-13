from django.db import models
from django.core.exceptions import ValidationError

from users.models import User


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
            ),
        ]

    def clean(self):
        if self.user == self.author:
            raise ValidationError(
                'Подписываться на себя нельзя в рамках данного сайта'
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        """Строковое представление модели"""

        return f'{self.user} {self.author}'
