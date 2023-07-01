from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from core.pagination import StandardResultsSetPagination

from .models import User
from .serializers import (ChangePasswordSerializer, PostUserSerializer,
                          UserSerializer)


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
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action == 'create':
            return PostUserSerializer  # has 'password' field

        return UserSerializer  # has 'is_subscribed' field

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
        lookup_field='email'
    )
    def me(self, request):
        self.kwargs.update(email=request.user.email)
        if request.method == 'PATCH':
            return self.partial_update(request, request.user.email)

        return self.retrieve(request, request.user.email)

    @action(["post"], detail=False, queryset=None)
    def set_password(self, request):
        user = self.request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            # Check old password
            if not user.check_password(
                serializer.data.get("current_password")
            ):
                return Response(
                    {"current_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get("new_password"))
            user.save()

            return Response(status=status.HTTP_204_NO_CONTENT)
