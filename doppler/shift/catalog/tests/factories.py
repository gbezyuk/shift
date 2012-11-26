"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: Model factories for tests
"""
import factory
from ..models import Image, Category, Product, Color, Size

class CategoryFactory(factory.Factory):
    """
    Category model factory
    """
    FACTORY_FOR = Category
    name = 'sample category'
    description = '<p>Simple <em>HTML-formatted</em> category description</p>'
    enabled = True
    parent = None
    slug = 'sample-category'

class ProductFactory(factory.Factory):
    """
    Product model factory
    """
    FACTORY_FOR = Product
    name = 'sample product'
    slug = 'sample-product'
    description = '<p>Simple <em>HTML-formatted</em> product description</p>'
    enabled = True

class ColorFactory(factory.Factory):
    """
    Color model factory
    """
    FACTORY_FOR = Color
    title = 'sample color'
    code = '#000000'

class SizeFactory(factory.Factory):
    """
    Size model factory
    """
    FACTORY_FOR = Size
    title = 'sample size'

class ImageFactory(factory.Factory):
    """
    Image model factory
    """
    FACTORY_FOR = Image
    title = 'sample image'
    enabled = True
    priority = False

from ..models import Shipment

class ShipmentFactory(factory.Factory):
    """
    Shipment model factory
    """
    FACTORY_FOR = Shipment
    special_price = 100
    remainder = 100
    enabled = True