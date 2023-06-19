from django.db import models

# for load default data use python manage.py loadingredients
class IngredientName(models.Model):
    name = models.CharField('Ingredient name', max_length=64)
    measurement_unit = models.CharField('Measurement unit', max_length=32)
