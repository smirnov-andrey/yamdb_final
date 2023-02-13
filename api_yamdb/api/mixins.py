from rest_framework import filters, mixins, viewsets

from .permissions import IsAdmin, IsReadOnly


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Определяет типовой миксин для вьюсетов."""
    permission_classes = [IsReadOnly | IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
