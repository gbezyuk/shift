from django.core.urlresolvers import reverse
from django.test import TestCase

class SkeletonTestCase(TestCase):

    def test_home(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

    def _test_wrong_uri_returns_404(self):
        response = self.client.get('/this/url/is/completely/wrong/')
        self.assertEqual(response.status_code, 404)