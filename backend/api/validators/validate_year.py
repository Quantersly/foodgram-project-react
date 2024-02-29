import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(value):
    """Валидатор created"""

    year = dt.date.today().year
    if not (value <= year):
        raise ValidationError('Указанная дата некорректна!')
    return value
