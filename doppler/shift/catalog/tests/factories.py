"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: Model factories for tests
"""
import factory
from ..models import Category

class CategoryFactory(factory.Factory):
    """
    Category model factory
    """
    FACTORY_FOR = Category
    name = 'category'
    description = '<p>Simple <em>HTML-formatted</em> category description</p>'
    enabled = True
    parent = None