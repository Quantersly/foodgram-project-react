import json

from django.conf import settings
from django.core.management import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        with open(
            f'{settings.BASE_DIR}/data/ingredients.json',
            'r', encoding='utf-8'
        ) as f:
            data = json.load(f)

            for row in data:
                if Ingredient.objects.filter(
                    name=row['name'],
                    measurement_unit=row['measurement_unit'],
                ) == []:
                    Ingredient.objects.bulk_create(
                        name=row['name'],
                        measurement_unit=row['measurement_unit'],
                    )
