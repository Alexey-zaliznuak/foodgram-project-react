from rest_framework.pagination import LimitOffsetPagination
from users.views import StandardResultsSetPagination
from django.http import FileResponse
from core import make_shopping_file
from rest_framework.decorators import action
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
)
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.http import FileResponse
from food.models import (
    Tag,
    Recipe,
    Favorite,
    Subscribe,
    Ingredient,
    ShoppingCart,
    IngredientAmount,
)
from rest_framework import (
    filters,
    viewsets,
)
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from .permissions import (
    IsAuthorOrReadOnlyPermission,
)
from .mixins_viewsets import (
    GetViewSet,
    ListCreateDeleteViewSet,
    CreateDestroyViewSet,
)
from .serializers import (
    # SubscribeSerializer,
    TagSerializer,
    IngredientSerializer,
    CreateShoppingCartRecipeSerializer,
    CreateFavoriteRecipeSerializer,
)


class IngredientViewSet(GetViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('^name',)

    serializer_class = IngredientSerializer


class TagViewSet(GetViewSet):
    queryset = Tag.objects.all()
    lookup_field = 'id'
    serializer_class = TagSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('^name',)

    serializer_class = TagSerializer


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

    @action(["get"], url_path='download_shopping_cart', detail=False)
    def download(self, request):
        cart = ShoppingCart.objects.filter(user=request.user)
        return FileResponse(make_shopping_file(cart))

# class SubscribeViewSet(ListCreateDeleteViewSet):
#     serializer_class = SubscribeSerializer
#     permission_classes = (IsAuthenticated,)
#     filter_backends = (filters.SearchFilter, )
#     search_fields = ('user__username', 'following__username')

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

#     def get_queryset(self):
#         return Subscribe.objects.filter(user=self.request.user)
