import braintree
from datetime import datetime

from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from .serializers import OrderSerializer, ConfirmOrderSerializer
from api_project.api.permissions import IsOwner
from orders.models import OrderItem, Order
from products.models import Product
from profiles.models import Address
from transactions.models import TransferPayment, BraintreePayment
from .extras import check_stocks
User = get_user_model()
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


class AddToCartAPIView(APIView):
    """ Add or update quatities of products to cart """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, product_pk):
        item = get_object_or_404(Product, pk=product_pk,
                                 stock__gt=0, available=True)

        if item.stock == 0:
            raise ValidationError(
                f'Sorry we\'re out stock for {item.name}')

        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=request.user,
            purchased=False
        )
        orders = Order.objects.filter(user=request.user, ordered=False)

        if orders.exists():
            order = orders[0]

            if order.orderitems.filter(item__id=item.id).exists():
                if order_item.quantity < item.stock:
                    order_item.quantity += 1
                    order_item.save()
                    serializer = OrderSerializer(order)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    raise ValidationError(
                        f'{item.name} stock is insuficient. We\'re sorry')
            else:
                order.orderitems.add(order_item)
                serializer = OrderSerializer(order)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            order = Order.objects.create(user=request.user)
            order.orderitems.add(order_item)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class RemoveFromCartAPIView(APIView):
    """
        Remove entire product from cart
        (the product and it's quantity)
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, product_pk):
        item = get_object_or_404(Product, pk=product_pk)
        orders = Order.objects.filter(user=request.user, ordered=False)

        if orders.exists():
            order = orders[0]
            if order.orderitems.filter(item__id=item.id).exists():
                orderitem = OrderItem.objects.filter(
                    item=item, user=request.user, purchased=False)[0]
                order.orderitems.remove(orderitem)
                orderitem.delete()

                if len(order.orderitems.all()) == 0:
                    order.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    serializer = OrderSerializer(order)
                    return Response(serializer.data,
                                    status=status.HTTP_200_OK)
            else:
                message = {'error': {
                    'code': 400,
                    'message': f'{item.name} was not in your cart'
                }}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            message = {'error': {
                'code': 400,
                'message': 'You don\'t have an active order'
            }}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class RemoveItemFromCartAPIView(APIView):
    """ Removes a single item from cart """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, product_pk):
        item = get_object_or_404(Product, pk=product_pk)
        orders = Order.objects.filter(user=request.user, ordered=False)

        if orders.exists():
            order = orders[0]
            if order.orderitems.filter(item__id=item.id).exists():
                order_item = OrderItem.objects.filter(
                    item=item, user=request.user, purchased=False)[0]

                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                else:
                    order.orderitems.remove(order_item)
                    if len(order.orderitems.all()) == 0:
                        order.delete()
                        return Response(status=status.HTTP_204_NO_CONTENT)

                serializer = OrderSerializer(order)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                message = {'error': {
                    'code': 400,
                    'message': f'{item.name} was not in your cart'
                }}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            message = {'error': {
                'code': 400,
                'message': 'You don\'t have an active order'
            }}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class ConfirmOrderAPIView(generics.RetrieveUpdateDestroyAPIView):
    """ Get order details to confirm and pay  """
    queryset = Order.objects.filter(ordered=False)
    serializer_class = ConfirmOrderSerializer
    permission_classes = (IsOwner,)

    def retrieve(self, request, *args, **kwargs):
        """ 
            Retrive order by pk
            Check it's stocks
            Create or retrieve braintree_client_id 
        """
        order = self.get_object()
        # Check stocks
        orderitems = order.orderitems.all()
        check_stocks(order, orderitems)
        # Create or retrieve a braintree_client_id
        user = request.user
        if not user.profile.braintree_customer_id:
            customer = gateway.customer.create({
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            })
            if customer.is_success:
                user.profile.braintree_customer_id = customer.customer.id
                user.save()
        braintree_customer_id = user.profile.braintree_customer_id
        client_token = gateway.client_token.generate({
            'customer_id': braintree_customer_id
        })

        serializer = self.get_serializer(order)
        res_dict = {**serializer.data,
                    'client_token': client_token}
        return Response(res_dict)

    def perform_update(self, serializer):
        """ 
            Updates with the shipping address and payment
            Most of the heavy lifting is made in the serializer
        """
        user = self.request.user
        serializer.save(user=user)

    def perform_destroy(self, instance):
        """ Destroy both the order and the orderitems """
        orderitems = instance.orderitems.all()
        # Delete the orderitems
        for i in orderitems:
            i.delete()

        instance.delete()
