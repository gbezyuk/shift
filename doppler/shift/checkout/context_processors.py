from .models import Cart

def cart(request):
    c = Cart.get_cart(request)
    return {
        'cart_distinct_quantity': c.total_distinct_quantity,
        'cart_total_quantity': c.total_quantity,
        'cart_total_price': c.total_price,
        'request': request
    }