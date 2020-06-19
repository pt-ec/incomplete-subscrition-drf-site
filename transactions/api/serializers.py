import re

from rest_framework import serializers

from transactions.models import (TransferPayment, BraintreePayment,
                                 SubscriptionPlan, Refund)


class TransferPaymentSerializer(serializers.ModelSerializer):
    """ Transfer payment model serializer  """
    class Meta:
        model = TransferPayment
        fields = '__all__'
        read_only_fields = ('created_at', 'payed_at')

    def validate(self, data):
        if data['iban'] and data['iban'] != '':
            if re.search("[^a-zA-Z0-9\s]", data['iban']):
                raise serializers.ValidationError(
                    'Iban must be only alphanumerical characters')

        return data


class BraintrePaymentSerializer(serializers.ModelSerializer):
    """ Braintree payment model serializer """
    class Meta:
        model = BraintreePayment
        fields = '__all__'
        read_only_fields = ('created_at', 'payed_at')


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    """ Subscription plan model serializer  """
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'
        read_only_fields = ('created_at',)
