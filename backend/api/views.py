from rest_framework.pagination import LimitOffsetPagination
from users.views import StandardResultsSetPagination
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
)
from .serializers import (
    # SubscribeSerializer,
    TagSerializer,
    IngredientSerializer,
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








# # Create your views here.
# class SubscribeViewSet(ListCreateDeleteViewSet):
#     serializer_class = SubscribeSerializer
#     permission_classes = (IsAuthenticated,)
#     filter_backends = (filters.SearchFilter, )
#     search_fields = ('user__username', 'following__username')

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

#     def get_queryset(self):
#         return Subscribe.objects.filter(user=self.request.user)

#
# #
# class PurchaseList(generics.ListAPIView):
#     serializer_class = PurchaseSerializer

#     def get_queryset(self):
#         """
#         This view should return a list of all the purchases
#         for the currently authenticated user.
#         """
#         user = self.request.user
#         return Purchase.objects.filter(purchaser=user)