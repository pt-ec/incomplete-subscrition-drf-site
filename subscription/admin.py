from django.contrib import admin

from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from .models import Category, Kit


class CategoryAdmin(admin.ModelAdmin):
    """ Kit category Admin register model """
    list_display = ('id', 'title', 'visible',)
    list_display_links = ('id', 'title',)
    search_fields = ('title',)
    list_filter = ('visible',)
    list_editable = ('visible',)
    list_per_page = 20


class ReviewsInline(admin.TabularInline):
    """ Edit the subcategory many to many relationship widget """
    model = Kit.reviews.through


class KitAdmin(admin.ModelAdmin, DynamicArrayMixin):
    """ Kit admin register model """
    list_display = ('id', 'name', 'new_member_stock', 'available',)
    list_display_links = ('id', 'name',)
    search_fields = ('name',)
    list_filter = ('available',)
    list_editable = ('available',)
    inlines = (
        ReviewsInline,
    )
    exclude = ('reviews',)
    list_per_page = 20


admin.site.register(Category, CategoryAdmin)
admin.site.register(Kit, KitAdmin)
