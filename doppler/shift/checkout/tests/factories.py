"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Checkout
Part: Model factories for tests
"""
import factory
from django.contrib.auth.models import User
from ..models import Cart, CartItem
from doppler.shift.catalog.tests.factories import ProductFactory, PriceFactory

class UserFactory(factory.Factory):
    """
    User model factory
    """
    FACTORY_FOR = User
    username = 'username'
    is_active = True

class CartFactory(factory.Factory):
    """
    Cart model factory
    """
    FACTORY_FOR = Cart

class CartItemFactory(factory.Factory):
    """
    CartItem model factory
    """
    FACTORY_FOR = CartItem
    quantity= 1