from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (VideoClassViewset,
                    VideoRetrieveAPIView,
                    VideoDetailAPIView,
                    VideoClassReviewCreateAPIView,
                    VideoClassReviewListAPIView,
                    VideoClassReviewDetailAPIView,
                    VideoCommentCreateAPIView,
                    VideoCommentListAPIView,
                    CommentVideoDetailAPIView)


router = DefaultRouter()
router.register(r'', VideoClassViewset,
                basename='video-classes')

urlpatterns = [
    path('classes/', include(router.urls)),

    path('classes/<int:video_class_pk>/review/',
         VideoClassReviewCreateAPIView.as_view(),
         name='review-video-class'),

    path('classes/<int:video_class_pk>/reviews/',
         VideoClassReviewListAPIView.as_view(),
         name='review-video-class'),

    path('class-reviews/<int:pk>/',
         VideoClassReviewDetailAPIView.as_view(),
         name='video-class-review'),

    path('videos/<int:pk>/',
         VideoRetrieveAPIView.as_view(),
         name='video'),

    path('videos/edit/<int:pk>/',
         VideoDetailAPIView.as_view(),
         name='video-edit'),

    path('videos/<int:video_pk>/comment/',
         VideoCommentCreateAPIView.as_view(),
         name='video-comment-create'),

    path('videos/<int:video_pk>/comments/',
         VideoCommentListAPIView.as_view(),
         name='video-comments'),

    path('video-comments/<int:pk>/',
         CommentVideoDetailAPIView.as_view(),
         name='video-comment'),
]
