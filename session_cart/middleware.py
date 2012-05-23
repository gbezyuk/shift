from session_cart.cart import Cart
from session_cart.utils import get_carts

class MultiCartMiddleware(object):
    """
    Middleware that handles adding session carts to the request object.
    """
    def process_request(self, request):
        """
        Add the carts to the request object.
        """
        request.carts = dict(
            (name, Cart(request, name))
            for name, Cart in get_carts().items()
        )

        if 'default' in get_carts():
            request.cart = request.carts['default']
        return None

    def process_response(self, request, response):
        """
        Update the session carts if they have changed.
        """
        # Don't assume the request object has carts, another layer may have
        # returned request this middleware's process_request was called.
        if hasattr(request, 'carts'):
            for name in get_carts():
                request.carts[name].save()
        return response

class SimpleCartMiddleware(object):
    """
    Middleware to support only a single cart, for the simple case
    """
    def process_request(self, request):
        request.cart = Cart(request)
        return None
    def process_response(self, request, response):
        if hasattr(request, 'cart'):
            request.cart.save()
        return response