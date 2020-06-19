from django.urls import include, path
from rest_framework.routers import DefaultRouter

from products.api.views import (CategoryViewSet,
                                SubcategoryViewSet,
                                ProductViewSet)


router = DefaultRouter()
router.register(r'categories', CategoryViewSet,
                basename='product-categories')
router.register(r'subcategories', SubcategoryViewSet,
                basename='product-subcategories')
router.register(r'products', ProductViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
]
