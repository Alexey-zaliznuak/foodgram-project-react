import pandas as pd
from django.core.management.base import BaseCommand
from food.models import Ingredient, Tag

# use this for load ingredients(-i) and tags(-t)
# python manage.py load -i -t


def loadcsv(file_name: str):
    return pd.read_csv(f'data/{file_name}.csv')


def import_ingredients():
    data = [
        Ingredient(
            name=row['name'],
            measurement_unit=row['measurement_unit'],
        )
        for i, row in loadcsv("ingredients").iterrows()
    ]
    Ingredient.objects.bulk_create(data)
    print('import ingredients completed successfully')


def import_tags():
    data = [
        Tag(
            name=row['name'],
            color=row['color'],
            slug=row['slug'],
        )
        for i, row in loadcsv("tags").iterrows()
    ]
    Tag.objects.bulk_create(data)
    print('import tags completed successfully')


class Command(BaseCommand):
    def handle(self, *args, **options):
        if options['ingredients']:
            import_ingredients()
        if options['tags']:
            import_tags()

    def add_arguments(self, parser):
        parser.add_argument(
            '-i',
            '--ingredients',
            action='store_true',
            default=False,
            help='load ingredients data'
        )
        parser.add_argument(
            '-t',
            '--tags',
            action='store_true',
            default=False,
            help='load tags data'
        )
