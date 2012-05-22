"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Checkout
Part: Models implementation
"""
from session_cart.cart import CartItem, Cart
CartItem.total_price = lambda self: self.item.value * self.quantity
Cart.total_price = lambda self: reduce(lambda res, x: res + x, [item.total_price() for item in self])