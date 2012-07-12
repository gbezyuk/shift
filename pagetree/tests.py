from django.core.urlresolvers import reverse
from django.test import TestCase
from .models import Page
import factory

class PageFactory(factory.Factory):
    FACTORY_FOR = Page

class PagetreeSimpleCase(TestCase):
    """
    Simple test cases for pagetree app
    """
    def test_page_available(self, page=None):
        """
        Enabled page with valid url should be available via its url
        """
        if not page:
            page = PageFactory(is_enabled=True, url="/valid_test_page_url/")
        resp = self.client.get(page.url)
        self.assertEqual(resp.status_code, 200, "Enabled page with valid url should be available via its url")

    def test_disabled_page_returns_404(self, page=None):
        """
        Disabled page should be unavailable via its url
        """
        if not page:
            page = PageFactory(is_enabled=False, url="/valid_test_page_url/")
        resp = self.client.get(page.url)
        self.assertEqual(resp.status_code, 404, "Disabled page should be unavailable via its url")

    def test_parent_disabling_disables_its_children(self):
        """
        Test that pages are organized as tree
        """
        root = PageFactory(is_enabled=True, url="/root/")
        child = PageFactory(is_enabled=False, url="/root/child/", parent=root)
        grandchild = PageFactory(is_enabled=True, url="/root/child/grandchild/", parent=child)
        self.test_page_available(root)
        self.test_disabled_page_returns_404(child)
        self.test_disabled_page_returns_404(grandchild)