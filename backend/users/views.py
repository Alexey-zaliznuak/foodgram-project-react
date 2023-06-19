from django.shortcuts import get_object_or_404

from .models import User
from .serializers import (
    UserSerializer,
    PostUserSerializer,
    ChangePasswordSerializer
)
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 1000


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter, )
    pagination_class = StandardResultsSetPagination

    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action == 'create':
            return PostUserSerializer # has 'password' field

        return UserSerializer

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

    @action(["post"], detail=False, queryset=None, serializer_class=ChangePasswordSerializer)
    def set_password(self, request):
        user = self.request.user
        serializer = ChangePasswordSerializer

        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get("new_password"))
            user.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

