from django_filters import (
    BooleanFilter,
    FilterSet,
    ModelChoiceFilter,
    ModelMultipleChoiceFilter
)
from food.models import Recipe, Tag
from users.models import User


class FilterRecipe(FilterSet):
    author = ModelChoiceFilter(queryset=User.objects.all())
    tags = ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(), to_field_name='slug'
    )
    is_favorited = BooleanFilter("is_favorited", method="is_favorited_filter")
    is_in_shopping_cart = BooleanFilter(
        "is_in_shopping_cart", method="is_in_shopping_cart_filter"
    )

    def is_favorited_filter(self, queryset, field_name, value):
        if self.request.user.is_authenticated() and value:
            queryset = queryset.filter(
                in_users_favorites__user=self.request.user
            )
        return queryset

    def is_in_shopping_cart_filter(self, queryset, field_name, value):
        if self.request.user.is_authenticated() and value:
            queryset = queryset.filter(
                in_shopping_cart__user=self.request.user
            )
        return queryset

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart',)
