from rest_framework import permissions
from rest_framework.generics import get_object_or_404

from subscription_classes.models import VideoClass


class IsSubscribed(permissions.IsAuthenticated):
    """ Check the current user to CUD but everyone can R """

    def has_object_permission(self, request, view, obj):
        is_authenticated = super().has_object_permission(request, view, obj)
        subscriptions = request.user.profile.subscriptions
        class_pk = view.kwargs.get('class_pk')
        video_class = get_object_or_404(VideoClass, pk=class_pk)
        subscription_plans = video_class.subscription_plans.all()
        subscribed = False

        for subscription_plan in subscription_plans:
            subscribed = subscriptions.filter(
                subscription_plan=subscription_plan).exists()
            if subscribed:
                break

        return is_authenticated and subscribed


class IsSubscribedOrReadOnly(permissions.BasePermission):
    """ Check if user is subscribed """

    def has_permission(self, request, view):
        class_pk = view.kwargs.get('class_pk')
        subscriptions = request.user.profile.subscriptions
        video_class = get_object_or_404(VideoClass, pk=class_pk)
        subscription_plans = video_class.subscription_plans.all()
        subscribed = False

        if request.method in permissions.SAFE_METHODS:
            return True

        for subscription_plan in subscription_plans:
            subscribed = subscriptions.filter(
                subscription_plan=subscription_plan).exists()
            if subscribed:
                break

        return subscribed
