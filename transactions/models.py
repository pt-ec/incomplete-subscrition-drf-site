from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class TransferPayment(models.Model):
    """ Transfer Payment data """
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             blank=True, null=True)
    amount = models.FloatField()
    iban = models.CharField(max_length=40, blank=True, null=True)
    payed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} {self.amount}€ payment'


class BraintreePayment(models.Model):
    """ Braintree Payment data """
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             blank=True, null=True)
    amount = models.FloatField()
    payed_at = models.DateTimeField(auto_now_add=True)
    braintree_id = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} {self.amount}€ payment'


class SubscriptionPlan(models.Model):
    """ User subscription model """
    relating_to = models.CharField(max_length=100)
    braintree_plan_id = models.CharField(max_length=50)
    braintree_plan_name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.braintree_plan_name} subscription'


class Refund(models.Model):
    """ Refund model """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    relating_to = models.CharField(max_length=100)
    reason = models.TextField(max_length=1000)
    accepted = models.BooleanField(default=False)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Refund for {self.order.id}'
