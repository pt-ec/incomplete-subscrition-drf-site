from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, KitViewSet,
                    CreateKitReviewAPIView,
                    SubscribeToKitAPIView,
                    KitReviewDetailAPIView)


router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='kit-categories')
router.register(r'', KitViewSet, basename='kits')

urlpatterns = [
    path('', include(router.urls)),

    path('<int:kit_pk>/subscribe',
         SubscribeToKitAPIView.as_view(),
         name='kit-subscribe'),

    path('<int:kit_pk>/review',
         CreateKitReviewAPIView.as_view(),
         name='kit-review'),

    path('reviews/<int:pk>/',
         KitReviewDetailAPIView.as_view(),
         name='kit-review-detail'),
]
