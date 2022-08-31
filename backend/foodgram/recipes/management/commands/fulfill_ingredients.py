import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('ingredients.csv', encoding='utf8') as file:
            reader = csv.reader(file, delimiter=';')
            next(reader)
            ingredients = []
            for row in reader:
                ingredients.append(
                    Ingredient(
                        name=row[0],
                        measurement_unit=row[1]
                    )
                )

        Ingredient.objects.bulk_create(ingredients)
