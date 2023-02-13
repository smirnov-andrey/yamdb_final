from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from .validators import username_validation

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
USERS_ROLES = [
    (USER, 'Аутентифицированный пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
]


class UserManager(BaseUserManager):
    def create_user(self, username, email, role, is_superuser=False,
                    password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            is_superuser=is_superuser,
            role=role,
            **kwargs,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, role='admin',
                         **kwargs):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            is_superuser=True,
            role=role,
            **kwargs,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(
        'Имя пользователя',
        max_length=settings.FIELD_LENGTH['username'],
        unique=True,
        blank=False,
        help_text=('Обязательное поле. Не более 30 символов. '
                   'Допускаются только буквы латинского алфавита, цифры и '
                   'символы @ . + - _'
                   ),
        validators=[username_validation],
        error_messages={'unique': 'Пользователь с таким именем уже существует'}
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=settings.FIELD_LENGTH['first_name'],
        blank=True)
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=settings.FIELD_LENGTH['last_name'],
        blank=True)
    email = models.EmailField(
        verbose_name='Email адрес',
        max_length=settings.FIELD_LENGTH['email'],
        blank=False,
        unique=True,
        help_text=('Указание email обязательно так как на него отправляется '
                   'ключ авторизации'))
    role = models.CharField(
        verbose_name='Права пользователя',
        blank=False,
        max_length=max(len(role) for role, title in USERS_ROLES),
        choices=USERS_ROLES,
        default=USER,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    is_superuser = models.BooleanField(
        verbose_name='Суперпользователь',
        default=False,
        help_text=('Обозначает, что у этого пользователя есть все разрешения'
                   'без их явного назначая.')
    )
    is_active = models.BooleanField(
        verbose_name='Активный пользователь',
        default=True,
        help_text=('Поле не доступно для редактирование администратором. '
                   'Активация осуществляется пользователем через API')
    )
    confirmation_code_hash = models.CharField(
        verbose_name='Хеш сумма кода подтверждения',
        blank=True,
        max_length=settings.FIELD_LENGTH['confirmation_code_hash']
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                name='unique_relationships',
                fields=['username', 'email'],
            ),
        ]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_staff(self):
        return self.is_superuser or self.role == ADMIN
