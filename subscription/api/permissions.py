from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from subscription.models import Kit, VideoClass


class KitIsSubscribedOrReadOnly(permissions.BasePermission):
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


class KitIsNotSubscribed(permissions.IsAuthenticated):
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


class ClassIsSubscribed(permissions.IsAuthenticated):
    """ Check the current user to CUD but everyone can R """

    def has_object_permission(self, request, view, obj):
        is_authenticated = super().has_object_permission(request, view, obj)
        subscriptions = request.user.profile.subscriptions
        class_pk = view.kwargs.get('class_pk')
        video_class = get_object_or_404(VideoClass, pk=class_pk)
        main_subscription = video_class.main_subscription_plan
        subscription_plans = video_class.subscription_plans.all()
        subscribed = False

        subscribed = subscriptions.filter(
            subscription_plan=main_subscription).exists()

        if not subscribed:
            for subscription_plan in subscription_plans:
                subscribed = subscriptions.filter(
                    subscription_plan=subscription_plan).exists()
                if subscribed:
                    break

        return is_authenticated and subscribed


class ClassIsSubscribedOrReadOnly(permissions.BasePermission):
    """ Check if user is subscribed """

    def has_permission(self, request, view):
        class_pk = view.kwargs.get('class_pk')
        subscriptions = request.user.profile.subscriptions
        video_class = get_object_or_404(VideoClass, pk=class_pk)
        main_subscription = video_class.main_subscription_plan
        subscription_plans = video_class.subscription_plans.all()
        subscribed = False

        if request.method in permissions.SAFE_METHODS:
            return True

        subscribed = subscriptions.filter(
            subscription_plan=main_subscription).exists()

        if not subscribed:
            for subscription_plan in subscription_plans:
                subscribed = subscriptions.filter(
                    subscription_plan=subscription_plan).exists()
                if subscribed:
                    break

        return subscribed


class ClassIsNotSubscribed(permissions.IsAuthenticated):
    """ Check if user is not subscribed """

    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        video_class_pk = view.kwargs.get('video_class_pk')
        subscriptions = request.user.profile.subscriptions
        video_class = get_object_or_404(VideoClass, pk=video_class_pk)
        subscription_plan = video_class.main_subscription_plan

        subscribed = subscriptions.filter(
            subscription_plan=subscription_plan).exists()

        return is_authenticated and not subscribed
