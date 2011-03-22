from satchmo_store.shop.models import Cart
from models import TieredDiscount

def tiered_discount(request):
    """Injects the valid tiered discount into the context"""

    cart = Cart.objects.from_request(request)
    discount = TieredDiscount.objects.valid(cart.total)
    if discount:
        amount = discount.amount(cart.total)
    else:
        amount = None

    return {
        'tiered_discount': discount,
        'tiered_discount_amount': amount,
    }

