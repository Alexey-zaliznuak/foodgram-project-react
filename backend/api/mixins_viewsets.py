from rest_framework import mixins
from rest_framework import viewsets


class GetViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    pass


class CreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass

class ListCreateDeleteViewSet(
    mixins.ListModelMixin,
    CreateDestroyViewSet,
):
    pass