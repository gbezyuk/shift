"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: View-related Tests
"""
from django.core.urlresolvers import reverse
from django.test import TestCase
from .models import Category

class CatalogTestCase(TestCase):
    """
    Catalog view tests
    """

    def setUp(self):
        #TODO: factory_boy-based categories. Root categories at first.
        pass

    def get_root_categories(self):
        return Category.root_visible.all()

    def test_index_page(self):
        """
        Test index page opens with Http 200 OK status
        """
        resp = self.client.get(reverse('doppler_shift_catalog_index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('root_categories' in resp.context)
        self.assertEqual([category.pk for category in resp.context['root_categories']],
            [category.pk for category in self.get_root_categories()])