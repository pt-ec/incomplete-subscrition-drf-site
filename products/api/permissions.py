from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.IsAdminUser):
    """ Check if user is admin or blocks it from Ppst, Put and Delete """

    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in permissions.SAFE_METHODS or is_admin
