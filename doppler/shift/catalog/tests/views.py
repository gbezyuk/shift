"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: View-related Tests
"""
from django.core.urlresolvers import reverse
from django.test import TestCase

class CatalogTestCase(TestCase):
    """
    Catalog view tests
    """

    def test_index_page(self):
        """
        Test index page opens with Http 200 OK status
        """
        resp = self.client.get(reverse('doppler_shift_catalog_index'))
        self.assertEqual(resp.status_code, 200)

