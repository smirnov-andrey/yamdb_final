from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User
from .validators import UsernameValidatorMixin

# Если вынести эти валидаторы в validators.py то будет кроссимпорт
UsernameUniqueValidator = UniqueValidator(
    queryset=User.objects.all(),
    message='Такое имя пользователя уже используется'
)
EmailUniqueValidator = UniqueValidator(
    queryset=User.objects.all(),
    message='Такой email уже используется'
)


class AuthSignupSerializer(serializers.Serializer, UsernameValidatorMixin):
    email = serializers.EmailField(
        max_length=settings.FIELD_LENGTH['email'])
    username = serializers.CharField(
        max_length=settings.FIELD_LENGTH['username'],
    )


class TokenGenerateSerializer(serializers.Serializer, UsernameValidatorMixin):
    username = serializers.CharField(
        max_length=settings.FIELD_LENGTH['username']
    )
    confirmation_code = serializers.CharField(
        max_length=settings.FIELD_LENGTH['confirmation_code']
    )


class UserSerializer(serializers.ModelSerializer, UsernameValidatorMixin):
    username = serializers.CharField(
        max_length=settings.FIELD_LENGTH['username'],
        required=True,
        validators=[UsernameUniqueValidator]
    )
    email = serializers.EmailField(
        max_length=settings.FIELD_LENGTH['email'],
        required=True,
        validators=[EmailUniqueValidator]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        lookup_field = 'username'


class UserMeSerializer(UserSerializer, UsernameValidatorMixin):
    # Переопределяем username и email так как для users/me они required=False
    # 4 строки ну ни как не получается
    username = serializers.CharField(
        max_length=settings.FIELD_LENGTH['username'],
        required=False,
        validators=[UsernameUniqueValidator]
    )
    email = serializers.EmailField(
        max_length=settings.FIELD_LENGTH['email'],
        required=False,
        validators=[EmailUniqueValidator]
    )

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role', )
