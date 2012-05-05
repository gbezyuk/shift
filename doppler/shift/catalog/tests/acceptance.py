"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: Acceptance integrational tests
"""
from django.core.urlresolvers import reverse
from django_webtest import WebTest

class IndexPageTest(WebTest):
    """
    Catalog index acceptance test
    """

    def test_index_view(self):
        """
        Test index page opens with Http 200 OK status
        """
        index_page = self.app.get(reverse('doppler_shift_catalog_index'))
        self.assertEqual(index_page.status, '200 OK')

