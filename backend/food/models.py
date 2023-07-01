from colorfield.fields import ColorField
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from models_config import (INGREDIENT_MEASUREMENT_UNIT_MAX_LENGTH,
                           INGREDIENT_NAME_MAX_LENGTH, MAX_COOKING_TIME,
                           RECIPE_NAME_MAX_LENGTH, TAG_NAME_MAX_LENGTH)
from users.models import User


# for load default data use python manage.py load -i -t (tags, ingredients)
class Ingredient(models.Model):
    # Name is not primary key because ingredient may have a duplicate
    # with another measurement unit.
    name = models.CharField(
        'Ingredient name', max_length=INGREDIENT_NAME_MAX_LENGTH
    )
    measurement_unit = models.CharField(
        'Measurement unit', max_length=INGREDIENT_MEASUREMENT_UNIT_MAX_LENGTH
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name="name_measurement_unit_unique"
            )
        ]

    def __str__(self) -> str:
        return self.name


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='amounts'
    )
    amount = models.PositiveIntegerField("amount", validators=[
        MinValueValidator(1),
    ])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('ingredient', "amount"),
                name="ingredient_amount_unique"
            )
        ]

    def __str__(self):
        return (
            f"{str(self.ingredient)} {self.amount} "
            f"{self.ingredient.measurement_unit}"
        )


class Tag(models.Model):
    name = models.CharField(
        'Tag for Recipes', max_length=TAG_NAME_MAX_LENGTH
    )
    color = ColorField('color', default='#FF0000')
    slug = models.SlugField("Slug", unique=True)

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name="author",
    )
    name = models.CharField("recipe name", max_length=RECIPE_NAME_MAX_LENGTH)
    image = models.ImageField(
        'image',
        upload_to='recipes/',
    )
    text = models.TextField('description')

    ingredients = models.ManyToManyField(
        IngredientAmount, verbose_name='ingredients'
    )

    tags = models.ManyToManyField(Tag, verbose_name="tags")
    cooking_time = models.PositiveSmallIntegerField(
        "cooking time(minute)",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(MAX_COOKING_TIME)
        ]
    )

    created = models.DateTimeField(
        "publication date",
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-created',)

    def __str__(self) -> str:
        return self.author.username + ' ' + self.name


class Subscribe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscribe_on')
    subscription = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscribers')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', "subscription"),
                name="user_subscription_unique"
            )
        ]

    def __str__(self) -> str:
        return f"{self.user} {self.subscription}"

    def clean(self):
        if self.user == self.subscription:
            raise ValidationError('You cant subsrite on yourself')


class FavoriteShoppingCartAbstart(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name='%(class)s')
    recipe = models.ForeignKey(
        Recipe, models.CASCADE, related_name='in_%(class)s'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.user} {self.recipe}"


class Favorite(FavoriteShoppingCartAbstart):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', "recipe"),
                name="user_recipe_%(class)s_unique"
            )
        ]


class ShoppingCart(FavoriteShoppingCartAbstart):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', "recipe"),
                name="user_recipe_%(class)s_unique"
            )
        ]
