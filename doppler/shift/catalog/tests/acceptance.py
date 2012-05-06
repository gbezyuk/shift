"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: Acceptance integrational tests
"""
from django.core.urlresolvers import reverse
from django_webtest import WebTest
from ..models import Category
from .factories import CategoryFactory
from django.template.response import ContentNotRenderedError

class IndexPageTest(WebTest):
    """
    Catalog index acceptance test
    """
    def setUp(self):
        self.root_category_enabled = CategoryFactory()
        self.child_category_enabled = CategoryFactory(parent=self.root_category_enabled)
        self.root_category_disabled= CategoryFactory(enabled=False)
        self.child_category_disabled = CategoryFactory(parent=self.root_category_disabled, enabled=False)

    def test_index_view(self):
        """
        Test index page opens with Http 200 OK status
        """
        index_page = self.app.get(reverse('doppler_shift_catalog_index'))
        self.assertEqual(index_page.status, '200 OK')
        self.assertIn(self.root_category_enabled.name, index_page)


    def test_enabled_category_view(self):
        """
        Test enabled category details page opens with Http 200 OK status
        """
        page = self.app.get(reverse('doppler_shift_catalog_category', kwargs={'category_id': self.root_category_enabled.id}))
        self.assertEqual(page.status, '200 OK')
        page = self.app.get(reverse('doppler_shift_catalog_category', kwargs={'category_id': self.child_category_enabled.id}))
        self.assertEqual(page.status, '200 OK')

    def test_disabled_category_view(self):
        """
        Test disabled category details page opens with Http 404 NOT FOUND status
        """
        self.assertRaises(ContentNotRenderedError, self.app.get,
            reverse('doppler_shift_catalog_category', kwargs={'category_id': self.root_category_disabled.id}))
        self.assertRaises(ContentNotRenderedError, self.app.get,
            reverse('doppler_shift_catalog_category', kwargs={'category_id': self.child_category_disabled.id}))