from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from reviews.models import Category, Genre, Review, Title

from .filters import TitleFilter
from .mixins import ListCreateDestroyViewSet
from .permissions import IsAdmin, IsAuthorModerator, IsReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleGetSerializer, TitlePostSerializer)


class CategoryViewSet(ListCreateDestroyViewSet):
    """Вьюсет для категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination


class GenreViewSet(ListCreateDestroyViewSet):
    """Вьюсет для жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""
    queryset = Title.objects.all().annotate(
        Avg('reviews__score')
    )
    permission_classes = [IsReadOnly | IsAdmin]
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter
                       )
    filterset_class = TitleFilter
    ordering_fields = ['name']

    def get_serializer_class(self):
        """определяем сериализатор в зависимости от типа запроса."""
        if self.action in ('retrieve', 'list'):
            return TitleGetSerializer
        return TitlePostSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = [IsReadOnly | IsAuthorModerator | IsAdmin]

    def get_title(self):
        return get_object_or_404(Title,
                                 id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев к отзывам."""
    serializer_class = CommentSerializer
    permission_classes = [IsReadOnly | IsAuthorModerator | IsAdmin]

    def get_review(self):
        return get_object_or_404(Review,
                                 id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
