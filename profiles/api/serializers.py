from django.contrib.auth import get_user_model
from rest_framework import serializers
from profiles.models import (Address, Review,
                             Profile, Subscription,
                             Comment)
User = get_user_model()


class AddressSerializer(serializers.ModelSerializer):
    """ Address model serializer """

    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ('created_at', 'user',
                            'address_type')


class UserSerializer(serializers.ModelSerializer):
    """ User model serializer """

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')
        read_only_fields = ('first_name', 'last_name')


class ReviewSerializer(serializers.ModelSerializer):
    """ Review model serializer """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at',)


class CommentSerializer(serializers.ModelSerializer):
    """ Comment model serializer """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at',)


class SubscriptionSerializer(serializers.ModelSerializer):
    """ 
        Subscription model serializer
        Test version without braintree
    """
    user = UserSerializer(read_only=True)
    # Billing Address related fields
    billing_address = AddressSerializer()
    save_billing = serializers.BooleanField(
        write_only=True, default=False)
    default_billing = serializers.BooleanField(
        write_only=True, default=False)
    # Shipping Address related fields
    same = serializers.BooleanField(
        write_only=True, default=False)
    shipping_address = AddressSerializer()
    save_shipping = serializers.BooleanField(
        write_only=True, default=False)
    default_shipping = serializers.BooleanField(
        write_only=True, default=False)

    class Meta:
        model = Subscription
        exclude = ('first_payment',)
        read_only_fields = ('start', 'active',
                            'subscription_plan',)

    def validate(self, data):
        """
            Check if address were provided
        """

        billing_address = data.get('billing_address')
        default_billing = data.get('default_billing')

        if not (billing_address or default_billing):
            raise serializers.ValidationError(
                'Please provide a billing address')

        same = data.get('same')
        shipping_address = data.get('shipping_address')
        default_shipping = data.get('default_shipping')

        if not (same or shipping_address or default_shipping):
            raise serializers.ValidationError(
                'Please provide a shipping address')

        return data
