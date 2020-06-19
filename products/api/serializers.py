from rest_framework import serializers
from products.models import Category, Subcategory, Product


class SubcategorySerializer(serializers.ModelSerializer):
    """ Subcategory model serializer """
    class Meta:
        model = Subcategory
        fields = '__all__'
        read_only_fields = ('created_at',)


class CategorySerializer(serializers.ModelSerializer):
    """ Category model serializer """
    subcategories = SubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('created_at',)


class ProductSerializer(serializers.ModelSerializer):
    """ Product model serializer """
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('created_at',)
