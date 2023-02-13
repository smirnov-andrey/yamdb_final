from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User

from .validators import my_year_validator


class CommonInfoCatGen(models.Model):
    name = models.CharField(
        max_length=settings.FIELD_LENGTH['name'],
        verbose_name='Наименование'
    )
    slug = models.SlugField(
        max_length=settings.FIELD_LENGTH['slug'],
        unique=True,
        verbose_name='Текстовый идентификатор'
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(CommonInfoCatGen):
    class Meta(CommonInfoCatGen.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CommonInfoCatGen):
    class Meta(CommonInfoCatGen.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.TextField(
        verbose_name='Наименование'
    )
    year = models.PositiveSmallIntegerField(
        validators=[my_year_validator],
        db_index=True,
        verbose_name='Год издания',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='genre',
        verbose_name='Жанр'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genretitle',
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='genretitle',
        verbose_name='Наименование'
    )

    def __str__(self):
        return f'{self.genre} {self.title}'


class CommonInfoRevCom(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        abstract = True
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:15]


class Review(CommonInfoRevCom):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,

        verbose_name='Произведение'
    )
    score = models.PositiveSmallIntegerField(
        null=True,
        validators=[
            MaxValueValidator(10, message='Оценка должна быть не выше 10'),
            MinValueValidator(1, message='Оценка должна быть не меньше 1')],
        verbose_name='Оценка',
        default=1
    )

    class Meta(CommonInfoRevCom.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]


class Comment(CommonInfoRevCom):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        verbose_name='Отзыв',
    )

    class Meta(CommonInfoRevCom.Meta):
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
