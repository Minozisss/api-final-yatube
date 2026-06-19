from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """Разрешаю всем читать, а менять только автору"""

    def has_object_permission(self, request, view, obj):
        """Проверяю что редактирует или удаляет именно автор"""
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
        )
