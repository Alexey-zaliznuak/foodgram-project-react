from django.db import models
from colorfield.fields import ColorField
from users.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


# for load default data use python manage.py loadingredients
class Ingredient(models.Model):
    # Name is not primary key because ingredient may have a duplicate
    # with another measurement unit.
    name = models.CharField('Ingredient name', max_length=64)
    measurement_unit = models.CharField('Measurement unit', max_length=32)

    def __str__(self) -> str:
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name="name_measurement_unit_unique"
            )
        ]

class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='amounts'
    )
    amount = models.PositiveIntegerField("amount", validators=[
            MinValueValidator(1)
        ]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('ingredient', "amount"),
                name="ingredient_amount_unique"
            )
        ]

    def __str__(self):
        return f"{self.ingredient} {self.amount}"

class Tag(models.Model):
    name = models.CharField('Tag for Recipes', max_length=32)
    color = ColorField('color', default='#FF0000')
    slug = models.SlugField("Slug", unique=True)

    def __str__(self) -> str:
        return self.name

class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name="Author",
    )
    name = models.CharField("recipe name", max_length=200)
    image = models.ImageField(
        'image',
        upload_to='recipes/',
    )
    text = models.TextField('description')
    ingredients = models.ManyToManyField(IngredientAmount)
    tags = models.ManyToManyField(Tag, verbose_name="tags")
    cooking_time = models.PositiveSmallIntegerField("cooking time(minute)")

    created = models.DateTimeField(
        "publication date",
        auto_now_add=True,
    )

    def __str__(self) -> str:
        return self.author.username + ' ' + self.name

    class Meta:
        ordering = ('-created',)

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

class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorites"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="is_favorite"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', "recipe"),
                name="user_recipe_unique"
            )
        ]

    def __str__(self):
        return f"{self.user} {self.recipe}"

class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="shopping_cart"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="in_shopping_cart"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', "recipe"),
                name="user_recipe_unique_shopping_cart"
            )
        ]
