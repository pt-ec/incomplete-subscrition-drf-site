from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, KitViewSet,
                    SubscribeToKitAPIView,
                    KitReviewCreateAPIView,
                    KitReviewListAPIView,
                    KitReviewDetailAPIView,
                    VideoClassViewset,
                    VideoRetrieveAPIView,
                    VideoDetailAPIView,
                    VideoClassReviewCreateAPIView,
                    VideoClassReviewListAPIView,
                    VideoClassReviewDetailAPIView,
                    VideoCommentCreateAPIView,
                    VideoCommentListAPIView,
                    VideoCommentDetailAPIView)


router = DefaultRouter()
router.register(r'classes', VideoClassViewset,
                basename='video-classes')
router.register(r'kit/categories', CategoryViewSet, basename='kit-categories')
router.register(r'kit', KitViewSet, basename='kits')

urlpatterns = [
    path('', include(router.urls)),

    path('kit/<int:kit_pk>/subscribe/',
         SubscribeToKitAPIView.as_view(),
         name='kit-subscribe'),

    path('kit/<int:kit_pk>/review/',
         KitReviewCreateAPIView.as_view(),
         name='kit-review-create'),

    path('kit/<int:kit_pk>/reviews/',
         KitReviewListAPIView.as_view(),
         name='kit-reviews'),

    path('kit-reviews/<int:pk>/',
         KitReviewDetailAPIView.as_view(),
         name='kit-review'),

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
         VideoCommentDetailAPIView.as_view(),
         name='video-comment'),
]
