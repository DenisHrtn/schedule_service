from rest_framework import permissions


class IsSuperuser(permissions.BasePermission):
    message = "You do not have permission to perform this action"

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False