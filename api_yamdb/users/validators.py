import re

from rest_framework.serializers import ValidationError


def username_validation(value):
    match_result = re.sub(r'([\w.@+-]+)', '', value)
    if not match_result == '':
        raise ValidationError(
            f'Поле username не должно содержать символы '
            f'{str(set(match_result)).strip("{}")}. Допускаются только '
            f'буквы латинского алфавита, цифры и символы @ . + - _'
        )
    if value == 'me':
        raise ValidationError(
            'Использовать имя "me" в качестве username запрещено.')
    return value


class UsernameValidatorMixin:

    def __init__(self, value):
        self.value = value

    def validate_username(self, value):
        username_validation(value)
        return value
