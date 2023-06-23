import base64
from rest_framework import serializers, validators
from django.core.files.base import ContentFile
from rest_framework.exceptions import ValidationError
from users.models import User
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
