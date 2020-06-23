from django.urls import include, path
from rest_framework.routers import DefaultRouter

from shop.api.views import (CategoryViewSet,
                            SubcategoryViewSet,
                            ProductViewSet,
                            AddToCartAPIView,
                            RemoveFromCartAPIView,
                            RemoveItemFromCartAPIView,
                            ConfirmOrderAPIView)


router = DefaultRouter()
router.register(r'categories', CategoryViewSet,
                basename='product-categories')
router.register(r'subcategories', SubcategoryViewSet,
                basename='product-subcategories')
router.register(r'products', ProductViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),

    path('products/<int:product_pk>/addtocart/',
         AddToCartAPIView.as_view(),
         name='add-to-cart'),

    path('products/<int:product_pk>/removefromcart/',
         RemoveFromCartAPIView.as_view(),
         name='remove-from-cart'),

    path('products/<int:product_pk>/removeitemfromcart/',
         RemoveItemFromCartAPIView.as_view(),
         name='remove-item-from-cart'),

    path('confirmorder/<int:pk>/',
         ConfirmOrderAPIView.as_view(),
         name='update-confirm-order'),
]
