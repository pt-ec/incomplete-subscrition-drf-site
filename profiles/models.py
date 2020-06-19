from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

from api_project.extras import schengen_area
from transactions.models import SubscriptionPlan, BraintreePayment
User = get_user_model()


class Address(models.Model):
    """ Save default billing address to user """
    ADDRESS_TYPE = [
        ('B', 'billing'),
        ('S', 'shipping'),
    ]
    SCHENGEN_AREA = schengen_area
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255, blank=True)
    zipcode = models.CharField(max_length=25)
    city = models.CharField(max_length=30)
    country = models.CharField(max_length=2, choices=SCHENGEN_AREA)
    address_type = models.CharField(max_length=1, choices=ADDRESS_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)


class Subscription(models.Model):
    """ Subscription Plan intermedy bebore addding to profile """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_plan = models.ForeignKey(
        SubscriptionPlan, on_delete=models.CASCADE)
    first_payment = models.ForeignKey(BraintreePayment, on_delete=models.SET_NULL,
                                      blank=True, null=True)
    billing_address = models.ForeignKey(Address, on_delete=models.SET_NULL,
                                        related_name='subscription_billing_address',
                                        blank=True, null=True)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL,
                                         related_name='subscription_shipping_address',
                                         blank=True, null=True)
    active = models.BooleanField(default=False)
    start = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subscription_plan.braintree_plan_name


class Profile(models.Model):
    """ Save customer user id """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    braintree_customer_id = models.CharField(
        max_length=50, blank=True, null=True)
    subscriptions = models.ManyToManyField(Subscription, blank=True)
    billing_address = models.ForeignKey(Address, on_delete=models.SET_NULL,
                                        related_name='default_billing_address',
                                        blank=True, null=True)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL,
                                         related_name='default_shipping_address',
                                         blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.email} profile'


class Review(models.Model):
    """ User review for various perpous """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),
                                                     MaxValueValidator(5)])
    comment = models.TextField(max_length=280, blank=True,
                               null=True, help_text="Maximum of 280 characters")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.email} review'


class Comment(models.Model):
    """ User comments for various perpous """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=280,
                            help_text="Maximum of 280 characters")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.email} comment'
