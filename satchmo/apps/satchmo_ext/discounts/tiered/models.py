from decimal import Decimal
import logging

from django.db import models
from django.template.defaultfilters import floatformat
from django.utils.translation import ugettext_lazy as _
from l10n.utils import moneyfmt

from satchmo_ext.discounts.common import DISCOUNT_AMOUNT, DISCOUNT_PERCENT, DISCOUNT_TYPES

log = logging.getLogger('satchmo_ext.discounts.tiered')

class TieredDiscountManager(models.Manager):

    def active(self):
        return self.filter(is_active=True)

    def valid(self, total):
        """Retrieves the discount tier that applies to the specified order"""

        if total > 0.0:
            possibles = self.active().filter(cart_minimum__lte=total)
            if len(possibles):
                return possibles[0]

        return None

class TieredDiscount(models.Model):
    cart_minimum = models.DecimalField(default=0.00, max_digits=18, decimal_places=10, help_text=_('Minimum cart value before this discount will apply'))
    discount = models.DecimalField(default=0.00, max_digits=18, decimal_places=10, help_text=_('The amount of the discount.  Percents are entered as whole numbers.'))
    discount_type = models.CharField(max_length=1, choices=DISCOUNT_TYPES, help_text=_('Select amount for a fixed amount discount, or select percent for discounts based on the total order value'))
    is_active = models.BooleanField(blank=True, default=True)

    objects = TieredDiscountManager()

    class Meta:
        ordering = ('-cart_minimum',)

    def __unicode__(self):
        if self.discount_type == DISCOUNT_AMOUNT:
            discount = moneyfmt(self.discount)
        else:
            discount = u'%s%%' % floatformat(self.discount)

        return u'%s off %s or more' % (discount, moneyfmt(self.cart_minimum))

    def amount(self, total):
        """Returns the discount amount"""

        amount = Decimal('0.0')
        if self.discount_type == DISCOUNT_AMOUNT:
            log.debug('Discounting a fixed amount: %s' % moneyfmt(self.discount))
            amount = self.discount
        elif self.discount_type == DISCOUNT_PERCENT:
            log.debug('Discounting by a percent of order total: %s' % self.discount)
            amount = total * self.discount / Decimal('100.0')

        return amount

