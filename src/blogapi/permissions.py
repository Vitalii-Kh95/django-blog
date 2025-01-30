from rest_framework import permissions


class IsAnonymous(permissions.BasePermission):
    """
    Permission that only grants access to requests from anonymous users.
    """

    message = "This action is only allowed for anonymous users."

    def has_permission(self, request, view):
        return not request.user.is_authenticated


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin users to perform unsafe methods.
    """

    def has_permission(self, request, view):
        # SAFE_METHODS are: GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow unsafe methods only for admin users
        return request.user and request.user.is_staff
