from rest_framework.exceptions import ValidationError


def check_stocks(order, orderitems):
    """
        Check stocks before going to purchase.
        This is a security measure if two people are buying
        the same product
    """
    difference = 0
    items = []
    for i in orderitems:
        difference = i.item.stock - i.quantity

        if difference < 0:
            items.append(i.item.name)

            if i.item.stock > 0:
                i.quantity = i.item.stock - abs(difference)
                i.save()
            else:
                order.orderitems.remove(i)
                if len(order.orderitems.all()) == 0:
                    order.delete()
    if difference != 0:
        item_string = ', '.join(items)
        raise ValidationError(f'{item_string} have just been bought.')
