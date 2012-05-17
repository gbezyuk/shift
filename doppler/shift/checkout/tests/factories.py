"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Checkout
Part: Model factories for tests
"""
import factory
from django.contrib.auth.models import User
from doppler.shift.catalog.tests.factories import ProductFactory, PriceFactory

class UserFactory(factory.Factory):
    """
    Category model factory
    """
    FACTORY_FOR = User
    username = 'username'
    is_active = True