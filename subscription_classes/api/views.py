from rest_framework import generics, viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import get_object_or_404

from api_project.api.permissions import (IsAdminUserOrReadOnly,
                                         IsOwnerOrReadOnly)
from api_project.api.pagination import NinePagination
from .serializers import (VideoSerializer, VideoClassSerializer,
                          VideoClassSectionSerializer,
                          VideoClassReviewSerializer,
                          VideoCommentSerializer)
from subscription_classes.models import (Video, VideoClass,
                                         VideoClassSection)
from .permissions import IsSubscribed
from profiles.models import Comment, Review


class VideoClassViewset(viewsets.ModelViewSet):
    """ Video class list create api view """
    queryset = VideoClass.objects.filter(visible=True)
    serializer_class = VideoClassSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    pagination_class = NinePagination
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = ('title', 'description',)
    ordering_fields = ('title', 'created_at')
    ordering = ('-created_at',)


class VideoRetrieveAPIView(generics.RetrieveAPIView):
    """ Video retrive api view """
    queryset = Video.objects.filter(visible=True)
    serializer_class = VideoSerializer
    permission_classes = (IsSubscribed,)


class ReviewVideoClassAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = VideoClassReviewSerializer
    permission_classes = (IsSubscribedOrReadOnly,)

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


class ReviewVideoClassDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """ Review a video class """
    queryset = Review.objects.all()
    serializer_class = VideoClassReviewSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class CommentVideoAPIView(generics.CreateAPIView):
    """ Create a comment in a video """
    queryset = Comment.objects.all()
    serializer_class = VideoCommentSerializer
    permission_classes = (IsSubscribed,)

    def perform_create(self, serializer):
        video_pk = self.kwargs.get('video_pk')
        video = get_object_or_404(Video, pk=video_pk)
        user = self.request.user

        serializer.save(user=user, video=video)


class CommentVideoDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """ Retrieve update destroy comment this Video """
    queryset = Comment.objects.all()
    serializer_class = VideoCommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)
