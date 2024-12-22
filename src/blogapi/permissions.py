from rest_framework.permissions import BasePermission


class IsAnonymous(BasePermission):
    """
    Permission that only grants access to requests from anonymous users.
    """

    def has_permission(self, request, view):
        return not request.user.is_authenticated
