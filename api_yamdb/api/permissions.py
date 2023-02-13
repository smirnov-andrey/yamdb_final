from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsReadOnly(BasePermission):
    """Разрешены только GET запросы на чтение list и detail."""
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS


class IsAuthorModerator(BasePermission):
    """Наличие прав автора, модератора, а так же разрешает POST."""
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.user.is_moderator


class IsAdmin(BasePermission):
    """Наличие прав админа или суперпользователя."""
    def has_permission(self, request, view):
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff
