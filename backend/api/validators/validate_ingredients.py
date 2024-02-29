from django.core.exceptions import ValidationError


def validate_ingredients(self, value):
    """Валидатор ingredients"""

    if not value:
        raise ValidationError('Добавьте ингридиент.')
    for i in value:
        if i['amount'] <= 0:
            raise ValidationError(
                'Количество ингредиентов не должно быть меньше 1'
            )
    return value
