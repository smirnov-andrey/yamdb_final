import csv

from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User

MYPATH = 'static/data'


class Command(BaseCommand):
    help = 'load data from csv'

    @staticmethod
    def read_csv(filename):
        """Функция для заполнения базы данных из csv файлов. """
        with open(MYPATH + '/' + filename, encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                if filename == 'genre.csv':
                    name = row['name']
                    slug = row['slug']
                    genre = Genre(name=name, slug=slug)
                    genre.save()
                if filename == 'category.csv':
                    name = row['name']
                    slug = row['slug']
                    category = Category(name=name, slug=slug)
                    category.save()
                if filename == 'titles.csv':
                    name = row['name']
                    year = row['year']
                    category = row['category']
                    title = Title(
                        name=name, year=year,
                        category=Category(id=category)
                    )
                    title.save()
                if filename == 'genre_title.csv':
                    genre_id = row['genre_id']
                    title_id = row['title_id']
                    genre_title = GenreTitle(
                        genre=Genre(id=genre_id),
                        title=Title(id=title_id)
                    )
                    genre_title.save()
                if filename == 'users.csv':
                    user_id = row['id']
                    username = row['username']
                    email = row['email']
                    role = row['role']
                    bio = row['bio']
                    first_name = row['first_name']
                    last_name = row['last_name']
                    user = User(
                        id=user_id, username=username, email=email,
                        role=role, bio=bio, first_name=first_name,
                        last_name=last_name,
                    )
                    user.save()
                if filename == 'review.csv':
                    title_id = row['title_id']
                    text = row['text']
                    author = row['author']
                    score = row['score']
                    pub_date = row['pub_date']
                    review = Review(
                        title=Title(id=title_id), text=text,
                        author=User(id=author), score=score, pub_date=pub_date,
                    )
                    review.save()
                if filename == 'comments.csv':
                    review_id = row['review_id']
                    text = row['text']
                    author = row['author']
                    pub_date = row['pub_date']
                    comment = Comment(
                        review=Review(id=review_id), text=text,
                        author=User(id=author), pub_date=pub_date,
                    )
                    comment.save()

    def handle(self, *args, **options):
        self.read_csv('category.csv')
        print('Таблица с жанрами заполнена')
        self.read_csv('genre.csv')
        print('Таблица с категориями заполнена')
        self.read_csv('titles.csv')
        print('Таблица с произведениями заполнена')
        self.read_csv('genre_title.csv')
        print('Вспомогательная таблица заполнена')
        self.read_csv('users.csv')
        print('Таблица с пользователями заполнена')
        self.read_csv('review.csv')
        print('Таблица с отзывами заполнена')
        self.read_csv('comments.csv')
        print('Таблица с коментариями к отзывам заполнена')
