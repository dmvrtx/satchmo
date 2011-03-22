import logging

from l10n.utils import moneyfmt
from satchmo_ext.discounts.common import DISCOUNT_AMOUNT, DISCOUNT_PERCENT
from satchmo_ext.discounts.signals import post_recalculate_total
from satchmo_store.shop.models import Order

from models import TieredDiscount

log = logging.getLogger('satchmo_ext.discounts.tiered')

def apply_discount(sender, instance, **kwargs):
    """Modifies the specified order's total discount based on the order's total value"""

    discount = TieredDiscount.objects.valid(instance.sub_total)
    if discount is not None:
        log.debug('Found a valid automatic discount: %s' % discount)
        log.debug('Order discount BEFORE processing: %s' % moneyfmt(instance.discount))

        amount = discount.amount(instance.sub_total)
        instance.discount += amount
        instance.total -= amount
        log.debug('Order discount AFTER processing: %s' % moneyfmt(instance.discount))
    else:
        log.debug('No valid automatic discounts found for this order')

post_recalculate_total.connect(apply_discount, sender=Order)

