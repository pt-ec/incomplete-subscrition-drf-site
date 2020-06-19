from django import forms
from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField


class Subcategory(models.Model):
    """ Product Subcategories """
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(
        null=False,
        unique=True,
        help_text="This is pre-populated with a slugified version of the title by default",
    )
    visible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "subcategories"


class Category(models.Model):
    """ Product Category """
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(
        null=False,
        unique=True,
        help_text="This is pre-populated with a slugified version of the title by default",
    )
    subcategories = models.ManyToManyField(Subcategory)
    visible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'categories'


class Product(models.Model):
    """ Product Models """
    # Units for measures and weight
    MEASURES_UNIT = [
        ('', 'Select Unit'),
        ('m', 'Meter'),
        ('dm', 'Decimeter'),
        ('cm', 'Centimeter'),
        ('mm', 'Millimeter'),
        ('in', 'Inches')
    ]
    WEIGHT_UNIT = [
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('lb', 'Pound'),
    ]
    # Base fields
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(
        null=False,
        unique=True,
        help_text="This is pre-populated with a slugified version of the name by default"
    )
    photo_1 = models.ImageField(
        upload_to='products/photos/%Y/%m/%d', verbose_name='Main Photo')
    photo_2 = models.ImageField(
        upload_to='products/photos/%Y/%m/%d', blank=True, null=True)
    photo_3 = models.ImageField(
        upload_to='products/photos/%Y/%m/%d', blank=True, null=True)
    photo_4 = models.ImageField(
        upload_to='products/photos/%Y/%m/%d', blank=True, null=True)
    photo_5 = models.ImageField(
        upload_to='products/photos/%Y/%m/%d', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)
    stock = models.IntegerField(default=1)
    unique = models.BooleanField(default=True)
    available = models.BooleanField(default=False)
    price = models.DecimalField(
        max_digits=14, decimal_places=2, default=10, help_text='In Euros (€)')
    created_at = models.DateTimeField(auto_now_add=True)
    # Materials
    materials = ArrayField(models.CharField(max_length=60))
    # Measures
    length = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        blank=True,
        null=True
    )
    length_unit = models.CharField(
        max_length=2,
        choices=MEASURES_UNIT,
        default=MEASURES_UNIT[0][0],
        blank=True,
    )
    width = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        blank=True,
        null=True
    )
    width_unit = models.CharField(
        max_length=2,
        choices=MEASURES_UNIT,
        default=MEASURES_UNIT[0][0],
        blank=True
    )
    height = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        blank=True,
        null=True
    )
    height_unit = models.CharField(
        max_length=2,
        choices=MEASURES_UNIT,
        default=MEASURES_UNIT[0][0],
        blank=True,
    )
    diameter = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        blank=True,
        null=True
    )
    diameter_unit = models.CharField(
        max_length=2,
        choices=MEASURES_UNIT,
        default=MEASURES_UNIT[0][0],
        blank=True,
    )
    # Weight
    weight = models.DecimalField(
        max_digits=9,
        decimal_places=2
    )
    weight_unit = models.CharField(
        max_length=2,
        choices=WEIGHT_UNIT,
        default=WEIGHT_UNIT[0][0]
    )

    def __str__(self):
        return self.name
