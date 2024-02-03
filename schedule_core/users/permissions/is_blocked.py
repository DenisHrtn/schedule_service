from rest_framework import permissions


class IsBlocked(permissions.BasePermission):
    message = 'You are blocked.'

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_blocked:
            return False
        return True