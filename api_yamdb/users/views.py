import hashlib
import uuid

from django.conf import settings
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (AuthSignupSerializer, TokenGenerateSerializer,
                          UserMeSerializer, UserSerializer)


@api_view(['POST'])
@permission_classes([AllowAny])
def auth_signup(request):
    """Обрабатывает API запросы на регистрацию новых пользователей."""
    serializer = AuthSignupSerializer(data=request.data, many=False)
    serializer.is_valid(raise_exception=True)
    try:
        user, created = User.objects.get_or_create(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email']
        )
    except IntegrityError:
        if User.objects.filter(
            username=serializer.validated_data['username']
        ).exists():
            response_data = {
                'username':
                    ['Пользователь с таким username уже существует']}
        else:
            response_data = {
                'email':
                    ['Пользователь с таким email уже существует']}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    confirmation_code = uuid.uuid4()
    hash_obj = hashlib.sha256()
    hash_obj.update(bytes(str(confirmation_code), 'utf-8'))
    confirmation_code_hash = hash_obj.hexdigest()
    send_mail(
        subject='API_YAMDB confirmation code',
        message=f'confirmation_code: {confirmation_code}',
        recipient_list=[serializer.validated_data['email']],
        from_email=settings.DEFAULT_FROM_EMAIL,
        fail_silently=False,
    )
    user.confirmation_code_hash = confirmation_code_hash
    user.is_active = True
    user.save()
    return Response(request.data, status=status.HTTP_200_OK)


class TokenGenerateView(APIView):
    """Выдает токен по API запросу авторизованного пользователя."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenGenerateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code_hash_obj = hashlib.sha256()
        confirmation_code_hash_obj.update(
            bytes(serializer.validated_data['confirmation_code'], 'utf-8'))
        confirmation_code_hash = confirmation_code_hash_obj.hexdigest()
        user = get_object_or_404(User, username=serializer.data['username'])
        if (user.confirmation_code_hash == confirmation_code_hash
                and not user.confirmation_code_hash == ''):
            refresh = RefreshToken.for_user(user)
            user.confirmation_code_hash = ''
            user.save()
            return Response({'token': str(refresh.access_token)},
                            status=status.HTTP_200_OK)
        return_data = {
            'confirmation_cod':
                ['Код подтверждения не действителен']}
        return Response(return_data,
                        status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    """Орабатывает API запросы админа по управлению пользователями"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminUser]
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('username', 'email', 'first_name', 'last_name', 'role')
    ordering_fields = ('username', 'email', 'first_name', 'last_name', 'role')
    lookup_field = 'username'

    @action(detail=False,
            methods=['GET', 'PATCH'],
            permission_classes=[IsAuthenticated],
            )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserMeSerializer(
                self.request.user,
                many=False,
                partial=True
            )
        if request.method == 'PATCH':
            serializer = UserMeSerializer(
                self.request.user,
                data=request.data,
                many=False
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
