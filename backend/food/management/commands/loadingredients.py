import pandas as pd
from django.core.management.base import BaseCommand

from food.models import IngredientName


def loadcsv(file_name:str):
    return pd.read_csv(f'data/{file_name}.csv')


def import_ingredients_names():
    data = [
        IngredientName(
            name=row[0],
            measurement_unit=row[1],
        )
        for i, row in loadcsv("ingredients").iterrows()
    ]
    IngredientName.objects.bulk_create(data)


class Command(BaseCommand):
    def handle(self, *args, **options):
        import_ingredients_names()
        print('import completed successfully')
