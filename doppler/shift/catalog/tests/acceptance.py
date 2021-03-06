"""
Studio: Doppler
Product: Shift e-commerce engine
Module: Catalog
Part: Acceptance integrational tests
"""
from django.core.urlresolvers import reverse
from django_webtest import WebTest
from doppler.shift.catalog.tests.factories import ProductFactory
from ..models import Category
from .factories import CategoryFactory
from django.template.response import ContentNotRenderedError

#TODO: make fixture-like inheritance or decrease shared models usage otherwise

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

class CategoryPageTest(WebTest):
    """
    Catalog category page acceptance test
    """
    def setUp(self):
        self.root_category_enabled = CategoryFactory()
        self.child_category_enabled = CategoryFactory(parent=self.root_category_enabled)
        self.root_category_disabled= CategoryFactory(enabled=False)
        self.child_category_disabled = CategoryFactory(parent=self.root_category_disabled, enabled=False)

    def test_root_category_view(self):
        """
        Test root category page opens with Http 200 OK status and contain proper insides
        """
        page = self.app.get(reverse('doppler_shift_catalog_category', kwargs={'category_id': self.root_category_enabled.pk}))
        self.assertEqual(page.status, '200 OK')
        self.assertIn(self.root_category_enabled.name, page)
        self.assertIn(self.root_category_enabled.description, page)
#        #TODO: add main image presence test here
#        if self.root_category_enabled.main_image:
#            self.assertIn(self.root_category_enabled.main_image.image.filename, page)
#        else:
#            print "test_root_category_view main image presence test skipped"
        self.assertIn(self.child_category_enabled.name, page)
        self.assertIn(self.child_category_enabled.description, page)
        self.assertIn(self.child_category_enabled.get_absolute_url(), page)

    def test_child_category_view(self):
        """
        Test child category page opens with Http 200 OK status and contain proper insides
        """
        product = ProductFactory(category=self.child_category_enabled)
        page = self.app.get(reverse('doppler_shift_catalog_category', kwargs={'category_id': self.child_category_enabled.pk}))
        self.assertEqual(page.status, '200 OK')
        self.assertIn(self.child_category_enabled.name, page)
        self.assertIn(self.child_category_enabled.description, page)
        #TODO: add main image presence test here
        self.assertIn(product.name, page)
        self.assertIn(product.get_absolute_url(), page)

    def test_root_category_breadcrumbs(self):
        """
        Test root category breadcrumbs
        """
        page = self.app.get(reverse('doppler_shift_catalog_category', kwargs={'category_id': self.root_category_enabled.pk}))
        for ancestor in self.root_category_enabled.get_ancestors(include_self=True):
            self.assertIn(ancestor.name, page)
            self.assertIn(ancestor.get_absolute_url(), page)

    def test_child_category_breadcrumbs(self):
        """
        Test root category breadcrumbs
        """
        page = self.app.get(reverse('doppler_shift_catalog_category', kwargs={'category_id': self.child_category_enabled.pk}))
        for ancestor in self.root_category_enabled.get_ancestors(include_self=True):
            self.assertIn(ancestor.name, page)
            self.assertIn(ancestor.get_absolute_url(), page)

class ProductPageTest(WebTest):
    """
    Catalog product page acceptance test
    """
    def setUp(self):
        self.root_category_enabled = CategoryFactory()
        self.child_category_enabled = CategoryFactory(parent=self.root_category_enabled)
        self.root_category_disabled= CategoryFactory(enabled=False)
        self.child_category_disabled = CategoryFactory(parent=self.root_category_disabled, enabled=False)

    def test_enable_product_inside_enabled_category(self):
        """
        Testing enabled product inside enabled category as a common case
        """
        product = ProductFactory(category=self.child_category_enabled)
        page = self.app.get(reverse('doppler_shift_catalog_product', kwargs={'product_id': product.pk}))
        self.assertIn(product.name, page)
        self.assertIn(product.description, page)

    def test_disabled_product_inside_enabled_category(self):
        """
        Testing disabled product inside enabled category raises 404
        """
        product = ProductFactory(category=self.child_category_enabled, enabled=False)
        self.assertRaises(ContentNotRenderedError, self.app.get,
            reverse('doppler_shift_catalog_product', kwargs={'product_id': product.pk}))

    def test_enabled_product_inside_disabled_category(self):
        """
        Testing enabled product inside disabled category raises 404
        """
        product = ProductFactory(category=self.child_category_disabled)
        self.assertRaises(ContentNotRenderedError, self.app.get,
            reverse('doppler_shift_catalog_product', kwargs={'product_id': product.pk}))

    def test_disabled_product_inside_disabled_category(self):
        """
        Testing disabled product inside disabled category raises 404
        """
        product = ProductFactory(category=self.child_category_disabled, enabled=False)
        self.assertRaises(ContentNotRenderedError, self.app.get,
            reverse('doppler_shift_catalog_product', kwargs={'product_id': product.pk}))

    def test_product_breadcrumbs(self):
        """
        Test product breadcrumbs
        """
        product = ProductFactory(category=self.child_category_enabled)
        page = self.app.get(reverse('doppler_shift_catalog_product', kwargs={'product_id': product.pk}))
        category = product.category
        for ancestor in category.get_ancestors(include_self=True):
            self.assertIn(ancestor.name, page)
            self.assertIn(ancestor.get_absolute_url(), page)
        self.assertIn(product.name, page)
        self.assertIn(product.get_absolute_url(), page)