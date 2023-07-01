from django_filters import (FilterSet, ModelChoiceFilter,
                            ModelMultipleChoiceFilter, NumberFilter)
from rest_framework import filters

from food.models import Recipe, Tag
from users.models import User


class FilterRecipe(FilterSet):
    author = ModelChoiceFilter(queryset=User.objects.all())
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_favorited = NumberFilter(max_value=1, method='filter_is_favorited')
    is_in_shopping_cart = NumberFilter(
        max_value=1, method='filter_is_in_shopping_cart'
    )

    def filter_is_favorited(self, queryset, field_name, value):
        if self.request.user.is_authenticated and value:
            queryset = queryset.filter(
                in_favorite__user=self.request.user
            )
        return queryset

    def filter_is_in_shopping_cart(self, queryset, field_name, value):
        if self.request.user.is_authenticated and value:
            queryset = queryset.filter(
                in_shoppingcart__user=self.request.user
            )
        return queryset

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart',)


class IngredientFilter(filters.SearchFilter):
    search_param = 'name'
