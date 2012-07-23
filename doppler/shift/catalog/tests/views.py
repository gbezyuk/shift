"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: View-related Tests
"""
from django.core.urlresolvers import reverse
from django.test import TestCase
from doppler.shift.catalog.tests.factories import ProductFactory
from .models import Category
from .factories import CategoryFactory
from django.template.response import ContentNotRenderedError

class CatalogTestCase(TestCase):
    """
    Catalog view tests
    """

    def setUp(self):
        self.root_category_enabled = CategoryFactory(slug='c1', enabled=True)
        self.child_category_enabled = CategoryFactory(parent=self.root_category_enabled, slug='c2')
        self.root_category_disabled= CategoryFactory(enabled=False, slug='c3')
        self.child_category_disabled = CategoryFactory(parent=self.root_category_disabled, enabled=False, slug='c4')
        self.child_category_product = ProductFactory(category=self.child_category_enabled, slug='c5')
        self.root_category_product = ProductFactory(category=self.root_category_enabled, slug='c6')

    def test_index_page(self):
        """
        Test index page opens with Http 200 OK status
        """
        resp = self.client.get(reverse('doppler_shift_catalog_index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('root_categories' in resp.context)
        self.assertEquals([category.pk for category in resp.context['root_categories']],
            [category.pk for category in Category.enabled_root.all()])

    def test_enabled_root_category_details_pages(self):
        """
        Test enabled root category details pages
        """
#        resp = self.client.get(reverse('doppler_shift_catalog_category',
#            kwargs={'category_id': self.root_category_enabled.id}))
        resp = self.client.get('/' + self.root_category_enabled.slug + '/')

        self.assertEqual(resp.status_code, 200)
        self.assertTrue('category' in resp.context)
        self.assertEqual(resp.context['category'], self.root_category_enabled)
        self.assertTrue('subcategories' in resp.context)
        self.assertEqual([c.pk for c in resp.context['subcategories']], [self.child_category_enabled.pk])

    def test_enabled_child_category_details_pages(self):
        """
        Test enabled child category details pages
        """
#        resp = self.client.get(reverse('doppler_shift_catalog_category',
#            kwargs={'category_id': self.child_category_enabled.id}))
        resp = self.client.get('/' + self.child_category_enabled.slug + '/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('category' in resp.context)
        self.assertEqual(resp.context['category'], self.child_category_enabled)
        self.assertTrue('products' in resp.context)
        self.assertEqual([p.pk for p in resp.context['products']], [self.child_category_product.pk])

    def test_disabled_category_details_pages(self):
        """
        Test disabled category details pages
        """
#        resp = self.client.get(reverse('doppler_shift_catalog_category',
#            kwargs={'category_id': self.root_category_disabled.id}))
        resp = self.client.get('/' + self.root_category_disabled.slug + '/')
        self.assertEqual(resp.status_code, 404)

        resp = self.client.get('/' + self.child_category_disabled.slug + '/')
#        resp = self.client.get(reverse('doppler_shift_catalog_category',
#            kwargs={'category_id': self.child_category_disabled.id}))
        self.assertEqual(resp.status_code, 404)

    def test_product_details_page(self):
        """
        Test product details page
        """
#        resp = self.client.get(reverse('doppler_shift_catalog_product',
#            kwargs={'product_id': self.root_category_product.id}))
        resp = self.client.get('/' + self.root_category_product.slug + '/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('category' in resp.context)
        self.assertEqual(resp.context['category'].pk, self.root_category_product.category.pk)
        self.assertTrue('product' in resp.context)
        self.assertEqual(resp.context['product'].pk, self.root_category_product.pk)