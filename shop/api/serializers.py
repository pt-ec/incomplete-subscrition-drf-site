from re import search
from datetime import datetime
import braintree

from django.conf import settings
from rest_framework import serializers

from shop.models import (Category, Subcategory, Product,
                         OrderItem, Order)
from profiles.models import Address
from profiles.api.serializers import AddressSerializer
from transactions.models import TransferPayment, BraintreePayment
from transactions.api.serializers import (TransferPaymentSerializer,
                                          BraintrePaymentSerializer)
from .utils import check_stocks
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


class SubcategorySerializer(serializers.ModelSerializer):
    """ Subcategory model serializer """
    class Meta:
        model = Subcategory
        fields = '__all__'
        read_only_fields = ('created_at',)


class CategorySerializer(serializers.ModelSerializer):
    """ Category model serializer """
    subcategories = SubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('created_at',)


class ProductSerializer(serializers.ModelSerializer):
    """ Product model serializer """
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('created_at',)


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'photo_1',
                  'unique', 'price')


class OrderItemSerializer(serializers.ModelSerializer):
    """ OrderItem model serializer """
    item = ItemSerializer(read_only=True)

    class Meta:
        model = OrderItem
        exclude = ('user',)
        read_only_fields = ('created_at',)


class OrderSerializer(serializers.ModelSerializer):
    """ Order model serializer """
    orderitems = OrderItemSerializer(many=True,
                                     read_only=True)
    billing_address = AddressSerializer(read_only=True,
                                        allow_null=True)
    shipping_address = AddressSerializer(read_only=True,
                                         allow_null=True)

    class Meta:
        model = Order
        exclude = ('braintree_payment', 'transfer_payment',)
        read_only_fields = ('created_at', 'user',)


class ConfirmOrderSerializer(serializers.ModelSerializer):
    """ Extension of order model serializer but with write fields """
    # order - orderitems relationship
    orderitems = OrderItemSerializer(many=True, read_only=True)
    # PAYMENT
    # nonce for braintree_payment
    payment_method_nonce = serializers.CharField(
        write_only=True, required=False)
    # iban for transfer_payment
    iban = serializers.CharField(
        write_only=True, max_length=35, required=False)
    # CHECKOUT ADDRESSES
    # billing address
    billing_address = AddressSerializer()
    save_billing = serializers.BooleanField(
        write_only=True, default=False)
    default_billing = serializers.BooleanField(
        write_only=True, default=False)
    # shipping address
    same = serializers.BooleanField(
        write_only=True, default=False)
    shipping_address = AddressSerializer()
    save_shipping = serializers.BooleanField(
        write_only=True, default=False)
    default_shipping = serializers.BooleanField(
        write_only=True, default=False)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('created_at', 'user', 'ordered_date',
                            'payed', 'shipped', 'received',
                            'refund_granted', 'canceled',
                            'transfer_payment', 'braintree_payment',
                            'refund_request', 'shipped_date',
                            'ordered')

    def validate(self, data):
        """
            Checks if iban exists and 
            only contains alphanumerical characters
        """
        iban = data.get('iban', '')
        if iban and search("[^a-zA-Z0-9\s]", iban):
            raise serializers.ValidationError(
                'Iban must be only alphanumerical characters')

        return data

    def update(self, instance, validated_data):
        """ Update order  """
        user = validated_data.pop('user')
        default_billing_address = user.profile.billing_address
        default_shipping_address = user.profile.shipping_address

        orderitems = instance.orderitems.all()
        check_stocks(instance, orderitems)

        # Billing Address Logic
        default_billing = validated_data.get('default_billing')
        if default_billing:
            if default_billing_address:
                billing_address = default_billing_address
            else:
                raise serializers.ValidationError(
                    'You don\'t have a default billing address')
        else:
            # Create a new billing_address
            billing_data = validated_data.pop('billing_address')
            billing_data.update(user=user, address_type='B')
            billing_address = Address.objects.create(**billing_data)
            save_billing = validated_data.get('save_billing')
            # Save to user instance
            if save_billing:
                user.profile.billing_address = billing_address
                user.profile.save()

        # Shipping Address Logic
        same = validated_data.get('same')
        default_shipping = validated_data.get('default_shipping')
        if default_shipping:
            if default_shipping_address:
                shipping_address = default_shipping_address
            else:
                raise serializers.ValidationError(
                    'You don\'t have a default shipping address')
        elif same:
            shipping_address = billing_address
            shipping_address.pk = None
            shipping_address.address_type = 'S'
            shipping_address.save()
        else:
            shipping_data = validated_data.pop('shipping_address')
            shipping_data.update(user=user, address_type='S')
            shipping_address = Address.objects.create(**shipping_data)
            save_shipping = validated_data.get('save_shipping')
            if save_shipping:
                user.profile.shipping_address = shipping_address
                user.profile.save()

        # Payment method Logic
        amount = instance.get_totals()
        payment_method = validated_data.get('payment_method')
        if payment_method == 'B':
            nonce = validated_data.get('payment_method_nonce')
            result = gateway.transaction.sale({
                'amount': f'{amount:.2f}',
                'payment_method_nonce': nonce,
                'options': {
                    'submit_for_settlement': True
                }
            })
            if result.is_success:
                braintree_payment = BraintreePayment(
                    user=user,
                    amount=amount,
                    braintree_id=user.braintreeuserprofile.braintree_customer_id
                )
                braintree_payment.save()
                instance.braintree_payment = braintree_payment
            else:
                raise serializers.ValidationError(
                    'Payment failed, you have\'t been charged')
        elif payment_method == 'T':
            transfer_payment = TransferPayment(
                user=user,
                amount=amount
            )
            iban = validated_data.get('iban')
            if iban:
                transfer_payment.iban = iban
            transfer_payment.save()
            instance.transfer_payment = transfer_payment

        instance.billing_address = billing_address
        instance.shipping_address = shipping_address
        instance.ordered = True
        instance.ordered_date = datetime.now()

        # update stocks
        for i in orderitems:
            current_stock = i.item.stock - i.quantity
            i.item.stock = current_stock
            i.purchased = True

            if current_stock == 0:
                i.item.available = False

            i.item.save()
            i.save()

        instance.save()

        return instance
