from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (BlogPostViewSet,
                    BlogPostCommentCreateAPIView,
                    BlogPostCommentListAPIView,
                    BlogPostCommentDetailAPIView)


router = DefaultRouter()
router.register(r'', BlogPostViewSet, basename='blog-posts')

urlpatterns = [
    path('', include(router.urls)),

    path('<int:blog_post_pk>/comment/',
         BlogPostCommentCreateAPIView.as_view(),
         name='blog-post-comment-create'),

    path('<int:blog_post_pk>/comments/',
         BlogPostCommentListAPIView.as_view(),
         name='blog-post-comments'),

    path('blog-post-comments/<int:pk>/',
         BlogPostCommentDetailAPIView.as_view(),
         name='blog-post-comment'),
]
