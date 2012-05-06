"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: Model-related Tests
"""
from django.core.urlresolvers import reverse
from django.test import TestCase
from .factories import CategoryFactory
from ..models import Category

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
