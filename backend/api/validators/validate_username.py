from django.core.exceptions import ValidationError


def validate_username(value):
    """Валидатор username"""

    if value.lower() == 'me':
        raise ValidationError(
            ('Имя пользователя не должно быть <me>'),
            params={'value': value},
        )
