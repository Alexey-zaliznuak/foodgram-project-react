from django.contrib.auth.models import Group
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from food.models import (
    Tag,
    Recipe,
    Favorite,
    Subscribe,
    Ingredient,
    ShoppingCart,
    IngredientAmount,
)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit', 'pk')
    list_filter = ('name', 'measurement_unit')
    search_fields = ('name',)


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'amount')
    list_filter = ('ingredient', 'amount')
    search_fields = ('ingredient', 'amount')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug', 'color_square')
    list_filter = ('name', 'slug')
    search_fields = ('name', 'slug')

    @admin.display(empty_value='unknown', description="square")
    def color_square(self, obj):
        return mark_safe(
            "<div id='square' style="
            f'"width: 30px; height: 30px; background-color: {obj.color}">'
            '</div>'
        )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author_link', 'image', 'ingredients_list', 'tags_list', 'cooking_time', 'created')
    search_fields = ('name',)

    @admin.display(description="author")
    def author_link(self, obj):
        url = reverse(
            'admin:users_user_change',
            kwargs={'object_id': obj.author.pk}
        )
        return mark_safe(
            f'<a target="_blank" href={url}>{obj.author}</a>'
        )

    @admin.display(description="ingredients")
    def ingredients_list(self, obj):
        res = ', '.join(
            [str(ingredient) for ingredient in obj.ingredients.all()]
        )

        return res

    @admin.display(description="tags")
    def tags_list(self, obj):
        res = ', '.join(
            [str(tag) for tag in obj.tags.all()]
        )

        return res


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription')
    search_fields = ('user', 'subscription')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')


admin.site.unregister(Group)
