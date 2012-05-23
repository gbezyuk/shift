from session_cart.utils import get_carts

def carts(request):
    """
    Returns all session carts as 'carts', and the default cart (if one is
    provided) as 'cart'.
    """
    context = {}
    carts = getattr(request, 'carts', None)
    cart = getattr(request, 'cart', None)
    if carts:
        if 'default' in get_carts():
            context['cart'] = carts['default']
        context['carts'] = carts
    elif cart:
        context['cart'] = cart
    return context