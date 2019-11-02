from rest_framework import permissions


class LoggedInPermission(permissions.BasePermission):
    """User must be logged in"""

    def has_permission(self, request, view):
        return request.user.id is not None


class NoPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True


class UserViewsPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'PUT' or request.method == 'GET':
            return request.user.id is not None
        return True
