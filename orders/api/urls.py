from django.urls import path
from .views import (AddToCartAPIView, RemoveFromCartAPIView,
                    RemoveItemFromCartAPIView,
                    ConfirmOrderAPIView)

urlpatterns = [
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
