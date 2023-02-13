import datetime as dt

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleGetSerializer(serializers.ModelSerializer):
    """Сериализатор произведений для метода GET."""
    genre = GenreSerializer(many=True)
    category = CategorySerializer(many=False)
    rating = serializers.IntegerField(
        source='reviews__score__avg',
        read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')
        read_only_fields = ('id', 'name', 'year', 'rating', 'description',
                            'genre', 'category')


class TitlePostSerializer(serializers.ModelSerializer):
    """Сериализатор произведений для методов кроме Get."""
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    @staticmethod
    def validate_year(value):
        year = dt.date.today().year
        if not value <= year:
            raise serializers.ValidationError('Проверьте год Произведения!')
        return value

    def to_representation(self, instance):
        return TitleGetSerializer(instance).data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    def validate(self, data):
        request = self.context['request']
        if request.method not in ('GET', 'PATCH'):
            author = request.user
            title_id = self.context['view'].kwargs.get('title_id')
            if Review.objects.filter(title_id=title_id,
                                     author=author).exists():
                raise ValidationError('Может существовать только один отзыв!')
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев на отзывы."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
