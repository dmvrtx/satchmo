from django.dispatch import Signal

post_recalculate_total = Signal(providing_args=['itemprices'])

