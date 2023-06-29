import base64

from users.models import User
from django.core.files.base import ContentFile
from django.db.models import Q
from food.models import (
    Tag,
    Recipe,
    Favorite,
    Subscribe,
    Ingredient,
    ShoppingCart,
    IngredientAmount,
)
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.utils import model_meta
from users.serializers import UserSerializer

WEEK = 60 * 24 * 7  # cooking_time for only the longest recipes


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
    name = serializers.CharField(source='ingredient.name')
    amount = serializers.IntegerField(min_value=1)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class CreateIngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), source='ingredient'
    )
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
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
                ingredient=ingredient.get("ingredient"),
                amount=ingredient.get("amount")
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


class SubscribeRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserGetSubscribeSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_is_subscribed(self, user):
        return Subscribe.objects.filter(
            Q(subscription=user) & Q(user=self.context['request'].user.id)
        ).exists()

    def get_recipes(self, user):
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')

        recipes = user.recipes.all()
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]

        context = {'request': request}
        return SubscribeRecipeSerializer(
            recipes, many=True,
            context=context
        ).data

    def get_recipes_count(self, user):
        return user.recipes.count()


class SubscribeSerializer(serializers.ModelSerializer):
    def validate(self, data):
        user = self.context['request'].user
        sub = self.instance

        if user == sub:
            raise ValidationError("You can`t subscribe on yourself")

        if Subscribe.objects.filter(
            Q(user=user) & Q(subscription=sub)
        ).exists():
            raise ValidationError("You already subscribe on this user")

        return data

    class Meta:
        model = Subscribe
        fields = (
            'id',
            'user',
            'subscription',
        )
        read_only_fields = ('user', 'subscription',)
