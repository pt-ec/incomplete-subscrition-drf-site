from rest_framework import generics, viewsets
from rest_framework.filters import SearchFilter, OrderingFilter

from .serializers import (CategorySerializer,
                          SubcategorySerializer,
                          ProductSerializer)
from .permissions import IsAdminUserOrReadOnly
from products.models import (Category,
                             Subcategory,
                             Product)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(visible=True).order_by('title')
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)


class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.filter(visible=True).order_by('title')
    serializer_class = SubcategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = ('name', 'description', 'price',)
    ordering_fields = ('name', 'price', 'created_at',)
    ordering = ('-created_at',)

    def get_queryset(self):
        queryset = Product.objects.filter(available=True,
                                          stock__gt=0)
        unique = self.request.query_params.get('unique', None)
        category = self.request.query_params.get('category', None)
        subcategory = self.request.query_params.get('subcategory', None)

        if unique is not None and unique is not False:
            queryset = queryset.filter(unique=True)

        if category is not None:
            queryset = queryset.filter(category__title__contains=category)

        if subcategory is not None:
            queryset = queryset.filter(
                subcategory__title__contains=subcategory)

        return queryset
