from django import forms
from django.db import models
from django.contrib.auth import get_user_model
from django_better_admin_arrayfield.models.fields import ArrayField

from profiles.models import Address
from transactions.models import (BraintreePayment, TransferPayment,
                                 Refund)
User = get_user_model()


class Subcategory(models.Model):
    """ Product Subcategories """
    title = models.CharField(max_length=150, unique=True)
    visible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "subcategories"


class Category(models.Model):
    """ Product Category """
    title = models.CharField(max_length=150, unique=True)
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
    name = models.CharField(max_length=250)
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


class OrderItem(models.Model):
    """ Order item model """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} of {self.item.name}'

    def get_total(self):
        total = self.item.price * self.quantity
        floattotal = float('{0:.2f}'.format(total))
        return floattotal


class Order(models.Model):
    PAYMENT_METHOD = [
        ('T', 'Bank Transfer'),
        ('B', 'Card or Paypal Payment')
    ]
    # BASE
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             blank=True, null=True)
    orderitems = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # ADDRESSES
    billing_address = models.ForeignKey(Address, on_delete=models.SET_NULL,
                                        related_name='billing_address',
                                        blank=True, null=True)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL,
                                         related_name='shipping_address',
                                         blank=True, null=True)
    # PAYMENT
    payment_method = models.CharField(max_length=1, choices=PAYMENT_METHOD)
    transfer_payment = models.ForeignKey(TransferPayment, on_delete=models.SET_NULL,
                                         blank=True, null=True)
    braintree_payment = models.ForeignKey(BraintreePayment, on_delete=models.SET_NULL,
                                          blank=True, null=True)
    payed = models.BooleanField(default=False)
    # SHIPPING
    shipped = models.BooleanField(default=False)
    shipped_date = models.DateTimeField(blank=True, null=True)
    received = models.BooleanField(default=False)
    # REFUND
    refund_request = models.ForeignKey(Refund, on_delete=models.SET_NULL,
                                       blank=True, null=True)
    refund_granted = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)

    def __str__(self):
        return f'Order {self.pk}'

    def get_totals(self):
        total = 0
        for order_item in self.orderitems.all():
            total += order_item.get_total()
        return total
