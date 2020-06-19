from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from .models import Category, Subcategory, Product


class SubcategoriesInline(admin.TabularInline):
    """ Edit the subcategory many to many relationship widget """
    model = Category.subcategories.through


class CategoryAdmin(admin.ModelAdmin):
    """ Register product category on admin area """
    list_display = ('id', 'title', 'visible',)
    list_display_links = ('id', 'title',)
    search_fields = ('title',)
    list_editable = ('visible',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = (
        SubcategoriesInline,
    )
    exclude = ('subcategories',)
    list_per_page = 20


class SubcategoryAdmin(admin.ModelAdmin):
    """ Register product subcategory on admin area """
    list_display = ('id', 'title',)
    list_display_links = ('id', 'title',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 20


class ProductAdmin(admin.ModelAdmin, DynamicArrayMixin):
    """ Register product  """
    fieldsets = (
        ('General:', {
            'fields': (
                'name',
                'slug',
                'photo_1',
                'photo_2',
                'photo_3',
                'photo_4',
                'photo_5',
                'category',
                'subcategory',
                'description',
                'stock',
                'unique',
                'available',
                'price',
            )
        }),
        ('Materials & Measures:', {
            'fields': (
                'materials',
                ('diameter', 'diameter_unit'),
                ('length', 'length_unit'),
                ('width', 'width_unit'),
                ('height', 'height_unit'),
                ('weight', 'weight_unit'),
            )
        }),
    )
    list_display = ('id', 'name', 'stock', 'available',)
    list_display_links = ('id', 'name',)
    search_fields = ('name', 'description',)
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20


admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Product, ProductAdmin)
