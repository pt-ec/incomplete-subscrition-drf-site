from django.db import models
from django.contrib.auth import get_user_model

from api_project.extras import schengen_area, payment_method
from products.models import Product
from profiles.models import Address
from transactions.models import (BraintreePayment, TransferPayment,
                                 Refund)
User = get_user_model()


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
    """ Order Model """
    # Choices
    PAYMENT_METHOD = payment_method
    SCHENGEN_AREA = schengen_area
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
