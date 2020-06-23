from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter

from core.api.permissions import IsAdminUserOrReadOnly, IsOwnerOrReadOnly
from core.api.pagination import ReviewPagination, ItemPagination, CommentPagination
from .serializers import (CategorySerializer, KitSerializer,
                          KitReviewSerializer,
                          KitSubscriptionSerializer,
                          VideoSerializer,
                          VideoClassSerializer,
                          VideoClassSectionSerializer,
                          SubscribeToVideoClassSerializer,
                          VideoClassReviewSerializer,
                          VideoCommentSerializer)
from .permissions import (KitIsSubscribedOrReadOnly, KitIsNotSubscribed,
                          ClassIsSubscribed, ClassIsSubscribedOrReadOnly,
                          ClassIsNotSubscribed)
from subscription.models import (Category, Kit,
                                 Video, VideoClass,
                                 VideoClassSection)
from profiles.models import Review, Subscription, Comment
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
    ordering = ('-created_at',)

    def get_queryset(self):
        queryset = Kit.objects.filter(available=True).order_by('-created_at')

        category = self.request.query_params.get('category', None)

        if category is not None:
            queryset = queryset.filter(category__title__contains=category)

        return queryset


class SubscribeToKitAPIView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = KitSubscriptionSerializer
    permission_classes = (KitIsNotSubscribed,)

    def perform_create(self, serializer):
        kit_pk = self.kwargs.get('kit_pk')
        kit = get_object_or_404(Kit, pk=kit_pk)
        user = self.request.user
        serializer.save(user=user, kit=kit)


class KitReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = KitReviewSerializer
    permission_classes = (KitIsSubscribedOrReadOnly,)

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


class KitReviewListAPIView(generics.ListAPIView):
    serializer_class = KitReviewSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = ReviewPagination
    filter_backends = (OrderingFilter,)
    ordering_fields = ('rating', 'created_at')
    ordering = ('-created_at',)

    def get_queryset(self):
        kit_pk = self.kwargs.get('kit_pk')
        kit = get_object_or_404(Kit, pk=kit_pk)
        return kit.reviews.all()


class KitReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = KitReviewSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class VideoClassViewset(viewsets.ModelViewSet):
    """ Video class list create api view """
    queryset = VideoClass.objects.filter(visible=True)
    serializer_class = VideoClassSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    pagination_class = ItemPagination
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = ('title', 'description',)
    ordering_fields = ('title', 'created_at')
    ordering = ('-created_at',)


class VideoRetrieveAPIView(generics.RetrieveAPIView):
    """ Video retrive api view """
    queryset = Video.objects.filter(visible=True)
    serializer_class = VideoSerializer
    permission_classes = (ClassIsSubscribed,)


class VideoDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """ Video detail api view """
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = (permissions.IsAdminUser,)


class SubscribeToVideoClassAPIView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscribeToVideoClassSerializer
    permission_classes = (ClassIsNotSubscribed,)

    def perform_create(self, serializer):
        video_class_pk = self.kwargs.get('video_class_pk')
        video_class = get_object_or_404(VideoClass, pk=video_class_pk)
        user = self.request.user
        serializer.save(user=user, video_class=video_class)


class VideoClassReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = VideoClassReviewSerializer
    permission_classes = (ClassIsSubscribedOrReadOnly,)

    def perform_create(self, serializer):
        video_class_pk = self.kwargs.get('video_class_pk')
        video_class = get_object_or_404(VideoClass, pk=video_class_pk)

        user = self.request.user
        subscription_plan = kit.subscription_plan

        kit_qs = Kit.objects.filter(reviews__user__contain=user)
        if kit_qs.exists():
            raise ValidationError(
                'You have already reviewed this kit')

        serializer.save(user=user, kit=kit)


class VideoClassReviewListAPIView(generics.ListAPIView):
    serializer_class = KitReviewSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = ReviewPagination
    filter_backends = (OrderingFilter,)
    ordering_fields = ('rating', 'created_at')
    ordering = ('-created_at',)

    def get_queryset(self):
        video_class_pk = self.kwargs.get('video_class_pk')
        video_class = get_object_or_404(VideoClass, pk=kit_pk)
        return video_class.reviews.all()


class VideoClassReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """ Review a video class """
    queryset = Review.objects.all()
    serializer_class = VideoClassReviewSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class VideoCommentCreateAPIView(generics.CreateAPIView):
    """ Create a comment in a video """
    queryset = Comment.objects.all()
    serializer_class = VideoCommentSerializer
    permission_classes = (ClassIsSubscribed,)

    def perform_create(self, serializer):
        video_pk = self.kwargs.get('video_pk')
        video = get_object_or_404(Video, pk=video_pk)
        user = self.request.user

        serializer.save(user=user, video=video)


class VideoCommentListAPIView(generics.ListAPIView):
    """ List the comments on a particular video """
    serializer_class = VideoCommentSerializer
    permissions_class = (IsOwnerOrReadOnly,)
    pagination_class = CommentPagination

    def get_queryset(self):
        video_pk = self.kwargs.get('video_pk')
        video = get_object_or_404(Video, pk=video_pk)
        return video.comments.all().order_by('-created_at')


class VideoCommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """ Retrieve update destroy comment this Video """
    queryset = Comment.objects.all()
    serializer_class = VideoCommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)
