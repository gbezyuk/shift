from django.conf import settings

CARTS = getattr(settings, 'SESSION_CARTS', {'default': 'session_cart.cart.Cart'})