from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from subscription_kits.models import Category, Kit


class IsSubscribedOrReadOnly(permissions.BasePermission):
    """ Check if user is subscribed """

    def has_permission(self, request, view):
        kit_pk = view.kwargs.get('kit_pk')
        subscriptions = request.user.profile.subscriptions
        kit = get_object_or_404(Kit, pk=kit_pk)
        subscription_plan = kit.subscription_plan

        if request.method in permissions.SAFE_METHODS:
            return True

        return subscriptions.filter(
            subscription_plan=subscription_plan).exists()


class IsNotSubscribed(permissions.IsAuthenticated):
    """ Check if user is not subscribed """

    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        kit_pk = view.kwargs.get('kit_pk')
        subscriptions = request.user.profile.subscriptions
        kit = get_object_or_404(Kit, pk=kit_pk)
        subscription_plan = kit.subscription_plan

        subscribed = subscriptions.filter(
            subscription_plan=subscription_plan).exists()

        return is_authenticated and not subscribed
