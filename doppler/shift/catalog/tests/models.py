"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: Model-related Tests
"""
from django.core.urlresolvers import reverse
from django.test import TestCase
from .factories import CategoryFactory, ProductFactory
from ..models import Category, Product, Price, MULTIPLE_PRICES

class CategoryTestCase(TestCase):
    """
    Tests for Category model
    """

    def setUp(self):
        """
        Initialization with a factory-provided set of models
        """
        self.root_category_enabled = CategoryFactory()
        self.child_category_enabled = CategoryFactory(parent=self.root_category_enabled)
        self.root_category_disabled= CategoryFactory(enabled=False)
        self.child_category_disabled = CategoryFactory(parent=self.root_category_disabled, enabled=False)

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

if MULTIPLE_PRICES:
    from .factories import PriceFactory
    
    class AdvancedPricingStrategyTestCase(TestCase):
        """
        Advanced pricing strategy test case
        """
        def setUp(self):
            """
            Initialization with a factory-provided set of models
            """
            self.sample_product = ProductFactory()
    
        def test_product_with_no_prices(self):
            """
            Product with no prices should return None as price
            """
            self.assertEqual(self.sample_product.price, None)
    
        def test_product_with_single_disabled_price(self):
            """
            Product with single disabled price should return None as price
            """
            PriceFactory(product=self.sample_product, enabled=False)
            self.assertEqual(self.sample_product.price, None)
    
        def test_product_with_many_disabled_prices(self):
            """
            Product with many disabled prices should return None as price
            """
            PriceFactory(product=self.sample_product, enabled=False)
            PriceFactory(product=self.sample_product, enabled=False)
            self.assertEqual(self.sample_product.price, None)
    
        def test_product_with_single_enabled_price(self):
            """
            Product with single enabled price should return that price's value as product price
            """
            price = PriceFactory(product=self.sample_product, enabled=True)
            self.assertEqual(self.sample_product.price, price.value)
    
        def test_product_with_many_enabled_prices(self):
            """
            Product with many enabled prices should return minimal price value as product price
            """
            min_price = PriceFactory(product=self.sample_product, enabled=True, value=100)
            PriceFactory(product=self.sample_product, enabled=True, value=1000)
            self.assertEqual(self.sample_product.price, min_price.value)
    
        def test_product_with_mixed_prices(self):
            """
            Product should return minimal enabled price value as product price
            """
            PriceFactory(product=self.sample_product, enabled=False, value=100)
            min_price = PriceFactory(product=self.sample_product, enabled=True, value=300)
            PriceFactory(product=self.sample_product, enabled=True, value=1000)
            self.assertEqual(self.sample_product.price, min_price.value)