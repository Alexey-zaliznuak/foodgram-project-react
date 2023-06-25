from api.filters import FilterRecipe
from core import make_shopping_file
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from food.models import (
    Favorite,
    Ingredient,
    Recipe,
    ShoppingCart,
    Tag
)
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from .serializers import (
    TagSerializer,
    RecipeSerializer,
    GetRecipeSerializer,
    IngredientSerializer,
    CreateFavoriteRecipeSerializer,
    CreateShoppingCartRecipeSerializer,
)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('^name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    lookup_field = 'id'
    serializer_class = TagSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('^name',)


class FavoriteViewSet(viewsets.ViewSet):
    @action(["post", "delete"], detail=True, url_path='favorite')
    def favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        if request.method == "POST":

            serializer = CreateFavoriteRecipeSerializer(
                recipe, data=request.data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)

            Favorite.objects.create(user=user, recipe=recipe)
            return Response(data=request.data, status=HTTP_201_CREATED)

        # delete favorite
        favorite = get_object_or_404(Favorite, user=user, recipe=recipe)
        favorite.delete()
        return Response(data=request.data, status=HTTP_204_NO_CONTENT)


class ShoppingCartViewSet(viewsets.ViewSet):
    @action(["post", "delete"], detail=True, url_path='shopping_cart')
    def shopping(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        if request.method == "POST":

            serializer = CreateShoppingCartRecipeSerializer(
                recipe, data=request.data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)

            ShoppingCart.objects.create(user=user, recipe=recipe)
            return Response(data=request.data, status=HTTP_201_CREATED)

        # delete recipe from shopping cart
        recipe = get_object_or_404(ShoppingCart, user=user, recipe=recipe)
        recipe.delete()
        return Response(data=request.data, status=HTTP_204_NO_CONTENT)

    @action(
        ["get"],
        url_path='download_shopping_cart',
        url_name='download_shopping_cart',
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        # Return txt file with list of needs ingredients
        cart = ShoppingCart.objects.filter(user=request.user)
        return FileResponse(make_shopping_file(cart))


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_set_class = FilterRecipe
    http_method_names = ["get", 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetRecipeSerializer

        return RecipeSerializer


# class SubscribeViewSet(ListCreateDeleteViewSet):
#     serializer_class = SubscribeSerializer
#     permission_classes = (IsAuthenticated,)
#     filter_backends = (filters.SearchFilter, )
#     search_fields = ('user__username', 'following__username')

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

#     def get_queryset(self):
#         return Subscribe.objects.filter(user=self.request.user)
