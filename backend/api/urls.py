from django.urls import path, include
from django.conf.urls import url

from rest_framework.routers import DefaultRouter as Router
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = Router()

urlpatterns = [
   path('', include(router.urls)),
   path('', include('users.urls')),
   # path('', include('djoser.urls')),
   path('', include('djoser.urls.authtoken')),
]

schema_view = get_schema_view(
   openapi.Info(
      title="Foodgram API",
      default_version='v1',
      description="Документация",
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
