from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (VideoClassViewset,
                    VideoRetrieveAPIView,
                    ReviewVideoClassAPIView,
                    ReviewVideoClassDetailAPIView,
                    CommentVideoAPIView,
                    CommentVideoDetailAPIView)

router = DefaultRouter()
router.register(r'video-classes', VideoClassViewset,
                basename='video-classes')


urlpatterns = [
    path('', include(router.urls)),

    path('<int:video_class_pk>/review/',
         ReviewVideoClassAPIView.as_view(),
         name='review-video-class'),

    path('reviews/<int:pk>/',
         ReviewVideoClassDetailAPIView.as_view(),
         name='video-class-review'),

    path('<int:class_pk>/video/<int:pk>/',
         VideoRetrieveAPIView.as_view(),
         name='video'),

    path('<int:class_pk>/video/<int:video_pk>/comment/',
         CommentVideoAPIView.as_view(),
         name='comment-video'),

    path('comments/<int:pk>/',
         CommentVideoDetailAPIView.as_view(),
         name='video-comment'),
]
