from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter

from api_project.api.permissions import IsAdminUserOrReadOnly, IsOwnerOrReadOnly
from .serializers import (CategorySerializer, KitSerializer,
                          KitReviewSerializer,
                          KitSubscriptionSerializer)
from .permissions import IsSubscribedOrReadOnly, IsNotSubscribed
from subscription_kits.models import Category, Kit
from profiles.models import Review, Subscription
User = get_user_model()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(visible=True).order_by('title')
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)


class KitViewSet(viewsets.ModelViewSet):
    serializer_class = KitSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (SearchFilter, OrderingFilter,)
    search_filters = ('name', 'description',
                      'products', 'price',)
    ordering_fields = ('name', 'price', 'created_at')
    ordering = ('-created_at')

    def get_queryset(self):
        queryset = Kit.objects.filter(available=True).order_by('-created_at')

        category = self.request.query_params.get('category', None)

        if category is not None:
            queryset = queryset.filter(category__title__contains=category)

        return queryset


class SubscribeToKitAPIView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = KitSubscriptionSerializer
    permission_classes = (IsNotSubscribed,)

    def perform_create(self, serializer):
        kit_pk = self.kwargs.get('kit_pk')
        kit = get_object_or_404(Kit, pk=kit_pk)
        user = self.request.user
        serializer.save(user=user, kit=kit)


class CreateKitReviewAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = KitReviewSerializer
    permission_classes = (IsSubscribedOrReadOnly,)

    def perform_create(self, serializer):
        kit_pk = self.kwargs.get('kit_pk')
        kit = get_object_or_404(Kit, pk=kit_pk)

        user = self.request.user
        subscription_plan = kit.subscription_plan

        kit_qs = Kit.objects.filter(reviews__user__contain=user)
        if kit_qs.exists():
            raise ValidationError(
                'You have already reviewed this kit')

        serializer.save(user=user, kit=kit)


class KitReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = KitReviewSerializer
    permission_classes = (IsOwnerOrReadOnly,)
