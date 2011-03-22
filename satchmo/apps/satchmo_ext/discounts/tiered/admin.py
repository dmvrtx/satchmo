from django.contrib import admin
from models import TieredDiscount, DISCOUNT_AMOUNT, DISCOUNT_PERCENT
from l10n.utils import moneyfmt

class TieredDiscountAdmin(admin.ModelAdmin):
    list_display = ('cart_min_currency', 'discount_str', 'is_active')
    list_filter = ('discount_type', 'is_active')

    def cart_min_currency(self, instance):
        return moneyfmt(instance.cart_minimum)

    cart_min_currency.short_description = u'Cart Minimum'

    def discount_str(self, instance):
        """Returns a string representing the discount based on its type"""

        if instance.discount_type == DISCOUNT_AMOUNT:
            return moneyfmt(instance.discount)
        elif instance.discount_type == DISCOUNT_PERCENT:
            return u'%s%%' % instance.discount
        else:
            return instance.discount

    discount_str.short_description = u'Discount'

admin.site.register(TieredDiscount, TieredDiscountAdmin)

