"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: Model factories for tests
"""
import factory
from ..models import Category, Product, MULTIPLE_PRICES

class CategoryFactory(factory.Factory):
    """
    Category model factory
    """
    FACTORY_FOR = Category
    name = 'sample category'
    description = '<p>Simple <em>HTML-formatted</em> category description</p>'
    enabled = True
    parent = None

class ProductFactory(factory.Factory):
    """
    Product model factory
    """
    FACTORY_FOR = Product
    name = 'sample product'
    description = '<p>Simple <em>HTML-formatted</em> product description</p>'
    enabled = True
    if not MULTIPLE_PRICES:
        price = 100

if MULTIPLE_PRICES:
    from ..models import Price

    class PriceFactory(factory.Factory):
        """
        Price model factory
        """
        FACTORY_FOR = Price
        note = 'sample price'
        value = 100
        enabled = True