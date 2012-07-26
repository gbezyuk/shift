from django.dispatch import Signal

order_created = Signal(providing_args=["order"])
order_state_changed = Signal(providing_args=["order"])