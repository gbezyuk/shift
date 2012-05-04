from django.core.urlresolvers import reverse
from django.test import TestCase

class SkeletonTestCase(TestCase):

    def test_home(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

