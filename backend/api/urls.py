from django.urls import path, include
from django.conf.urls import url

from rest_framework.routers import DefaultRouter as Router
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api.views import(
   IngredientViewSet,
   TagViewSet,
   FavoriteViewSet,
   ShoppingCartViewSet,
   RecipeViewSet,
)

router = Router()
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', ShoppingCartViewSet, basename='shoppingcarts')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('recipes', FavoriteViewSet, basename='favorites')
router.register('ingredients', IngredientViewSet, basename='ingredients')


urlpatterns = [
   path('', include(router.urls)),
   path('', include('users.urls')),
   path('auth/', include('djoser.urls.authtoken')),
]

schema_view = get_schema_view(
   openapi.Info(
      title="Foodgram API",
      default_version='v1',
      description="Documentation",
      # terms_of_service="URL страницы с пользовательским соглашением",
      contact=openapi.Contact(email="zaliznuak50@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),

   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
   url(r'^swagger(?P<format>\.json|\.yaml)$',
      schema_view.without_ui(cache_timeout=0), name='schema-json'),
   url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
      name='schema-swagger-ui'),
]
