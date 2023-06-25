from django.shortcuts import get_object_or_404

from .models import User
from .serializers import (
    UserSerializer,
    PostUserSerializer,
    ChangePasswordSerializer
)
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework import pagination
from rest_framework import mixins
from rest_framework import viewsets
from core import StandardResultsSetPagination


class UserMixin(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    pass


class UserViewSet(UserMixin):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter, )
    pagination_class = StandardResultsSetPagination

    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action == 'create':
            return PostUserSerializer # has 'password' field

        return UserSerializer # has 'is_subscribed' field

    def get_permissions(self):
        if self.action == 'create':
            return (AllowAny(),)

        return super().get_permissions()

    @action(
        methods=['PATCH', 'GET'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        filter_backends=(),
        pagination_class=None,
        serializer_class=UserSerializer,
    )
    def me(self, request):
        self.kwargs.update(username=request.user.username)
        if request.method == 'PATCH':
            return self.partial_update(request, request.user.username)

        return self.retrieve(request, request.user.username)

    @action(["post"], detail=False, queryset=None)
    def set_password(self, request):
        user = self.request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            # Check old password
            if not user.check_password(serializer.data.get("current_password")):
                return Response(
                    {"current_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get("new_password"))
            user.save()

            return Response(status=status.HTTP_200_OK)
