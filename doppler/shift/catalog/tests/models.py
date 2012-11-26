"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: Model-related Tests
"""
from django.db.utils import IntegrityError
from django.test import TestCase
from .factories import CategoryFactory, ProductFactory, ImageFactory, ColorFactory, SizeFactory
from ..models import Category, Image

class CategoryTestCase(TestCase):
    """
    Tests for Category model
    """

    def setUp(self):
        """
        Initialization with a factory-provided set of models
        """
        self.root_category_enabled = CategoryFactory(slug='c1')
        self.child_category_enabled = CategoryFactory(parent=self.root_category_enabled, slug='c2')
        self.root_category_disabled= CategoryFactory(enabled=False, slug='c3')
        self.child_category_disabled = CategoryFactory(parent=self.root_category_disabled, enabled=False, slug='c4')

    def test_enabled_tree(self):
        """
        Testing enabled tree manager
        """
        self.assertEquals([self.root_category_enabled.pk, self.child_category_enabled.pk],
            [id for id in Category.enabled_tree.all().values_list('id', flat=True)])

    def test_enabled_root(self):
        """
        Testing enabled root manager
        """
        self.assertEquals([self.root_category_enabled.pk],
            [id for id in Category.enabled_root.all().values_list('id', flat=True)])

    def test_enabled_products(self):
        """
        Testing enabled products filtering property
        """
        p1 = ProductFactory(category=self.root_category_enabled, enabled=True, slug='p1')
        p2 = ProductFactory(category=self.root_category_enabled, enabled=True, slug='p2')
        ProductFactory(category=self.root_category_enabled, enabled=False)
        self.assertEqual([p1.pk, p2.pk], [product.id for product in self.root_category_enabled.enabled_products])

class ImagesTestCase(TestCase):
    """
    Image model related tests
    """
    def setUp(self):
        """
        Initialization with a factory-provided set of models
        """
        self.sample_product = ProductFactory()

    def test_product_with_no_images(self):
        """
        Product with no images should return None as image
        """
        self.assertEqual(self.sample_product.main_image, None)
        self.assertEqual(Image.get_main_image_for_object(self.sample_product), None)

    def test_product_with_single_disabled_image(self):
        """
        Product with single disabled image should return None as image
        """
        ImageFactory(content_object=self.sample_product, enabled=False)
        self.assertEqual(self.sample_product.main_image, None)
        self.assertEqual(Image.get_main_image_for_object(self.sample_product), None)

    def test_product_with_multiple_disabled_images(self):
        """
        Product with multiple disabled images should return None as image
        """
        ImageFactory(content_object=self.sample_product, enabled=False)
        ImageFactory(content_object=self.sample_product, enabled=False)
        ImageFactory(content_object=self.sample_product, enabled=False)
        self.assertEqual(self.sample_product.main_image, None)
        self.assertEqual(Image.get_main_image_for_object(self.sample_product), None)

    def test_product_with_single_enabled_image(self):
        """
        Product with single enabled image should return this image as main
        """
        image = ImageFactory(content_object=self.sample_product, enabled=True)
        self.assertEqual(self.sample_product.main_image, image)
        self.assertEqual(Image.get_main_image_for_object(self.sample_product), image)

    def test_enabled_images_priority(self):
        """
        Product with multiple enabled images should return priority image as main
        """
        ImageFactory(content_object=self.sample_product, enabled=True)
        image = ImageFactory(content_object=self.sample_product, enabled=True, priority=True)
        self.assertEqual(self.sample_product.main_image, image)
        self.assertEqual(Image.get_main_image_for_object(self.sample_product), image)

    def test_product_enabled_images(self):
        """
        Product model property 'enabled_images'  should return filtered enabled images only
        """
        ImageFactory(content_object=self.sample_product, enabled=False)
        ImageFactory(content_object=self.sample_product, enabled=False)
        i1 = ImageFactory(content_object=self.sample_product, enabled=True)
        i2 = ImageFactory(content_object=self.sample_product, enabled=True)
        self.assertEqual([i1.pk, i2.pk], [i.pk for i in self.sample_product.enabled_images])

    def test_mixed_case(self):
        """
        Product with multiple images should return enabled random priority image as main
        """
        ImageFactory(content_object=self.sample_product, enabled=True)
        ImageFactory(content_object=self.sample_product, enabled=False)
        image = ImageFactory(content_object=self.sample_product, enabled=True, priority=True)
        self.assertEqual(self.sample_product.main_image, image)
        self.assertEqual(Image.get_main_image_for_object(self.sample_product), image)
        ImageFactory(content_object=self.sample_product, enabled=True, priority=True)
        self.assert_(self.sample_product.main_image)
        self.assert_(Image.get_main_image_for_object(self.sample_product))

from .factories import ShipmentFactory

class AdvancedPricingStrategyTestCase(TestCase):
    """
    Advanced pricing strategy test case
    """
    def setUp(self):
        """
        Initialization with a factory-provided set of models
        """
        self.sample_product = ProductFactory()

    def test_product_price_values_unique(self):
        """
        Make sure IntegrityError is thrown where necessary on unique_together constraint
        """
        c = ColorFactory()
        s = SizeFactory()
        ShipmentFactory(product=self.sample_product, value=1)
        ShipmentFactory(product=self.sample_product, value=1, color=c)
        ShipmentFactory(product=self.sample_product, value=1, color=c, size=s)
        self.assertRaises(IntegrityError, ShipmentFactory, product=self.sample_product, value=1, color=c, size=s)

    def test_product_with_no_prices(self):
        """
        Product with no prices should return None as price
        """
        self.assertEqual(self.sample_product.price, None)

    def test_product_with_single_disabled_price(self):
        """
        Product with single disabled price should return None as price
        """
        ShipmentFactory(product=self.sample_product, enabled=False)
        self.assertEqual(self.sample_product.price, None)

    def test_product_with_many_disabled_prices(self):
        """
        Product with many disabled prices should return None as price
        """
        ShipmentFactory(product=self.sample_product, enabled=False, value=1)
        ShipmentFactory(product=self.sample_product, enabled=False, value=2)
        self.assertEqual(self.sample_product.price, None)

    def test_product_with_single_enabled_price(self):
        """
        Product with single enabled price should return that price's value as product price
        """
        price = ShipmentFactory(product=self.sample_product, enabled=True)
        self.assertEqual(self.sample_product.price, price.value)

    def test_product_with_many_enabled_prices(self):
        """
        Product with many enabled prices should return minimal price value as product price
        """
        min_price = ShipmentFactory(product=self.sample_product, enabled=True, value=100)
        ShipmentFactory(product=self.sample_product, enabled=True, value=1000)
        self.assertEqual(self.sample_product.price, min_price.value)

    def test_product_with_mixed_prices(self):
        """
        Product should return minimal enabled price value as product price
        """
        ShipmentFactory(product=self.sample_product, enabled=False, value=100)
        min_price = ShipmentFactory(product=self.sample_product, enabled=True, value=300)
        ShipmentFactory(product=self.sample_product, enabled=True, value=1000)
        self.assertEqual(self.sample_product.price, min_price.value)