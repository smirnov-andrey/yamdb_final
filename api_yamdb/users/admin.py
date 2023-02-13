from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group

from .models import User


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput
    )
    email = forms.CharField(
        label='Email адрес',
        widget=forms.EmailInput,
        help_text=('Указание email обязательно так как на него отправляется '
                   'ключ авторизации')
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name',
                  'last_name', 'role', 'bio')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label='Пароль',
        help_text=('Пароли пользователей не хранятся в текстовом виде, '
                   'поэтому пароль этого пользователя невозможно увидеть, '
                   'но вы можете изменить пароль, используя <b><a '
                   'href=\"../password/\">ЭТУ ФОРМУ</a></b>.')
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name',
                  'last_name', 'role', 'bio')

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'role', 'is_superuser')
    list_filter = ('role', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'last_name', 'bio')}),
        ('Разрешения', {'fields': ('role', 'is_superuser', 'is_active')}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'last_name', 'bio')}),
        ('Разрешения', {'fields': ('role', 'is_superuser', 'is_active')}),
    )
    search_fields = ('username', 'email', 'password', 'first_name',
                     'last_name')
    ordering = ('username',)
    filter_horizontal = ()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['is_active'].disabled = True
        if request.user.is_superuser is not None:
            form.base_fields['is_superuser'].disabled = True
        if obj is not None and request.user.username == obj.username:
            form.base_fields['is_superuser'].disabled = True
            form.base_fields['role'].disabled = True
        return form


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
