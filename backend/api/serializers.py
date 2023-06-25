import base64
from rest_framework import serializers, validators
from django.core.files.base import ContentFile
from rest_framework.exceptions import ValidationError
from rest_framework.utils import model_meta
from users.serializers import UserSerializer
from django.db.models import Q, Model
from food.models import (
    Tag,
    Recipe,
    Favorite,
    Subscribe,
    Ingredient,
    ShoppingCart,
    IngredientAmount,
)


WEEK = 60 * 24 * 7 # cooking_time for only the longest recipes


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag

class CreateFavoriteRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        read_only_fields = ('name', 'image', 'cooking_time')
        fields = ('id', *read_only_fields)
        model = Recipe

    def validate(self, data):
        user = self.context['request'].user
        recipe = self.instance

        if Favorite.objects.filter(Q(user=user) & Q(recipe=recipe)).exists():
            raise ValidationError("This recipe already in favorites")

        return data

class CreateShoppingCartRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        read_only_fields = ('name', 'image', 'cooking_time')
        fields = ('id', *read_only_fields)
        model = Recipe

    def validate(self, data):
        user = self.context['request'].user
        recipe = self.instance

        if ShoppingCart.objects.filter(
            Q(user=user) & Q(recipe=recipe)
        ).exists():
            raise ValidationError("This recipe already in shopping cart")

        return data

class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(source = 'ingredient.name')
    amount = serializers.IntegerField(min_value = 1)
    measurement_unit = serializers.CharField(source = 'ingredient.measurement_unit')

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount',)

class CreateIngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all(), source='ingredient')
    amount = serializers.IntegerField(min_value = 1)

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')

class RecipeSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    ingredients = CreateIngredientAmountSerializer(many=True)
    name = serializers.CharField(min_length=3, max_length=64,)
    image = Base64ImageField(required=False, allow_null=True)
    text = serializers.CharField()
    cooking_time = serializers.IntegerField(min_value=1, max_value=WEEK)


    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')

        recipe = Recipe.objects.create(**validated_data)

        ingredients = self.convert_ingredients_to_ingredients_amounts(
            ingredients
        )

        recipe.tags.set(tags)
        recipe.ingredients.set(ingredients)

        return recipe

    def update(self, instance, validated_data):
        info = model_meta.get_field_info(instance)

        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save()

        # Note that many-to-many fields are set after updating instance.
        # Setting m2m fields triggers signals which could potentially change
        # updated instance and we do not want it to collide with .update()

        for attr, value in m2m_fields:
            field = getattr(instance, attr)

            if attr == 'ingredients':
                value = self.convert_ingredients_to_ingredients_amounts(value)

            field.set(value)

        return instance

    def convert_ingredients_to_ingredients_amounts(self, ingredients):
        # convert list elements like
        # OrderedDict([('ingredient', <Ingredient: ...>), ('amount', ...)])
        # on IngredientAmount objects
        for index, ingredient in enumerate(ingredients):
            ingredients[index], _ = IngredientAmount.objects.get_or_create(
                ingredient = ingredient.get("ingredient"),
                amount = ingredient.get("amount")
            )

        return ingredients

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        read_only_fields = ('id', 'author')

class GetRecipeSerializer(RecipeSerializer):
    author = UserSerializer()
    tags = TagSerializer(many=True)
    ingredients = IngredientAmountSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart',
        )
        read_only_fields = ('id', 'author')

    def get_is_favorited(self, recipe):
        return Favorite.objects.filter(
            Q(user=self.context['request'].user.id) & Q(recipe=recipe)
        ).exists()

    def get_is_in_shopping_cart(self, recipe):
        return ShoppingCart.objects.filter(
            Q(user=self.context['request'].user.id) & Q(recipe=recipe)
        ).exists()


# class SubscribeSerializer(serializers.ModelSerializer):
#     subscribers = serializers.SlugRelatedField(
#     #     slug_field='username',
#     #     queryset=User.objects.all(),
#     # )

#     def validate_following(self, value):
#         if self.context["request"].user == value:
#             raise serializers.ValidationError(
#                 'You are trying to subscribe to yourself.'
#                 '(you set yourself in "following")'
#             )
#         return value

#     class Meta:
#         fields = '__all__'
#         model = Subscribe
#         validators = [
#             validators.UniqueTogetherValidator(
#                 queryset=Follow.objects.all(),
#                 fields=('user', 'following')
#             )
#         ]
