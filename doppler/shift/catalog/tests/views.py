"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: View-related Tests
"""
from django.core.urlresolvers import reverse
from django.test import TestCase
from .models import Category
from .factories import CategoryFactory

class CatalogTestCase(TestCase):
    """
    Catalog view tests
    """

    def setUp(self):
        self.root_category_enabled = CategoryFactory()
        self.child_category_enabled = CategoryFactory(parent=self.root_category_enabled)
        self.root_category_disabled= CategoryFactory(enabled=False)
        self.child_category_disabled = CategoryFactory(parent=self.root_category_disabled, enabled=False)

    def test_index_page(self):
        """
        Test index page opens with Http 200 OK status
        """
        resp = self.client.get(reverse('doppler_shift_catalog_index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('root_categories' in resp.context)
        self.assertEquals([category.pk for category in resp.context['root_categories']],
            [category.pk for category in Category.enabled_root.all()])