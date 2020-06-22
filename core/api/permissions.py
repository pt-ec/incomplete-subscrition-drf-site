from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.IsAdminUser):
    """ Check if user is admin or blocks it from Post, Put and Delete """

    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in permissions.SAFE_METHODS or is_admin


class IsOwner(permissions.BasePermission):
    """ Check the current user to the user foreign key of a given model """
    message = 'You are not the owner'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    """ Check the current user to CUD but everyone can R """

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS or
                obj.user == request.user)
