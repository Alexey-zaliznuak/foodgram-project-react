from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from core.make_shopping_file import make_shopping_file
from core.pagination import StandardResultsSetPagination
from food.models import (Favorite, Ingredient, Recipe, ShoppingCart, Subscribe,
                         Tag)
from users.models import User

from .filters import FilterRecipe, IngredientFilter
from .permissions import IsAuthorOrReadOnly
from .serializers import (CreateFavoriteRecipeSerializer,
                          CreateShoppingCartRecipeSerializer,
                          GetRecipeSerializer, IngredientSerializer,
                          RecipeSerializer, SubscribeSerializer, TagSerializer,
                          UserGetSubscribeSerializer)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [IngredientFilter]
    search_fields = ('^name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    lookup_field = 'id'
    serializer_class = TagSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('^name',)


class FavoriteViewSet(viewsets.ViewSet):
    @action(
        ["post", "delete"],
        detail=True,
        url_path='favorite',
        permission_classes=(IsAuthenticated,)
    )
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
    @action(
        ["post", "delete"],
        True,
        url_path='shopping_cart',
        permission_classes=(IsAuthenticated,)
    )
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
    filterset_class = FilterRecipe
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)
    pagination_class = StandardResultsSetPagination
    http_method_names = ["get", 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetRecipeSerializer

        return RecipeSerializer


class GetSubscriptions(
    viewsets.mixins.ListModelMixin, viewsets.GenericViewSet
):
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.SearchFilter,)
    serializer_class = UserGetSubscribeSerializer

    def get_queryset(self):
        user = self.request.user
        new_queryset = [sub.subscription for sub in user.subscribe_on.all()]
        print(new_queryset, new_queryset[0].recipes_count)
        return new_queryset


class SubscribeViewSet(viewsets.ViewSet):
    @action(["post", "delete"], detail=True, url_path='subscribe')
    def subscribe(self, request, pk):
        user = request.user
        sub = get_object_or_404(User, id=pk)

        if request.method == "POST":

            serializer = SubscribeSerializer(
                sub, data=request.data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)

            Subscribe.objects.create(user=user, subscription=sub)
            response_data = UserGetSubscribeSerializer(
                sub,
                context={'request': request}
            ).to_representation(sub)
            return Response(
                data=response_data, status=HTTP_201_CREATED
            )

        # delete subscribe
        sub = get_object_or_404(Subscribe, user=user, subscription=sub)
        sub.delete()
        return Response(data=request.data, status=HTTP_204_NO_CONTENT)
