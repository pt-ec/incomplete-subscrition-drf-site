from rest_framework import serializers
from subscription_kits.models import Category, Kit
from profiles.models import Review, Address, Subscription
from profiles.api.serializers import (ReviewSerializer,
                                      SubscriptionSerializer)


class CategorySerializer(serializers.ModelSerializer):
    """ Category model serializer """
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('created_at',)


class KitSerializer(serializers.ModelSerializer):
    """ Kit model serializer """
    reviews = ReviewSerializer(read_only=True, many=True)

    class Meta:
        model = Kit
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at',)


class KitSubscriptionSerializer(SubscriptionSerializer):
    """ Kit subscription serializer (prototype without payment) """

    def create(self, validated_data):
        kit = validated_data.pop('kit')
        subscription_plan = kit.subscription_plan
        user = validated_data.pop('user')

        subscription = Subscription(user=user, active=True,
                                    subscription_plan=subscription_plan)
        default_billing = validated_data.get('default_billing', False)
        if default_billing and user.profile.billing_address:
            billing_data = user.profile.billing_address
            subscription.billing_address = billing_data
        else:
            billing_data = validated_data.get('billing_address')
            billing_data.update(user=user)
            billing_address = Address.objects.create(**billing_data)
            subscription.billing_address = billing_address
            if validated_data.get('save_billing', False):
                user.profile.billing_address = billing_address

        same = validated_data.get('same', False)
        default_shipping = validated_data.get('default_shipping', False)
        if same:
            if billing_data == user.profile.billing_address:
                subscription.shipping_address = billing_data
            else:
                subscription.shipping_address = billing_address
        elif default_shipping and user.profile.shipping_address:
            shipping_data = user.profile.shipping_address
            subscription.shipping_address = shipping_data
        else:
            shipping_data = validated_data.get('shipping_address')
            shipping_data.update(user=user)
            shipping_address = Address.objects.create(**billing_data)
            subscription.shipping_address = shipping_address
            if validated_data.get('save_shipping', False):
                user.profile.shipping_address = shipping_address

        subscription.save()
        user.profile.subscriptions.add(subscription)
        user.save()
        return subscription


class KitReviewSerializer(ReviewSerializer):
    """ Kit Review Serializer creation """

    def create(self, validated_data):
        kit = validated_data.pop('kit')
        review = Review.objects.create(**validated_data)
        kit.reviews.add(review)
        return review
