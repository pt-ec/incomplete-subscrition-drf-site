from django.contrib import admin

from .models import TransferPayment, SubscriptionPlan


admin.site.register(SubscriptionPlan)
admin.site.register(TransferPayment)
