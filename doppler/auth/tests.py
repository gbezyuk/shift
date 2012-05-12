"""
Studio: Doppler
Module: Basic user authorization
Part: Tests
"""
from django.core.urlresolvers import reverse
from django_webtest import WebTest
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
import factory

class UserFactory(factory.Factory):
    """
    User model factory
    """
    FACTORY_FOR = User
    username = 'sample_user'
    active = True

class AuthAcceptanceTest(WebTest):
    """
    Acceptance test for login and logout functionality
    """
    def test_login_link_present_for_anonymous_user(self):
        """
        test login link present for anonymous user
        """
        page = self.app.get('/')
        self.assertIn(_('login'), page)
        self.assertIn(reverse('doppler_auth_login'), page)

    def test_logout_link_does_not_present_for_anonymous_user(self):
        """
        test logout link does not present for anonymous user
        """
        page = self.app.get('/')
        self.assertNotIn(_('logout'), page)
        self.assertNotIn(reverse('doppler_auth_logout'), page)

    def test_logout_link_present_for_authorized_user(self):
        """
        test logout link present for authorized user
        """
        page = self.app.get('/', user=UserFactory())
        self.assertIn(_('logout'), page)
        self.assertIn(reverse('doppler_auth_logout'), page)

    def test_login_link_does_not_present_for_authorized_user(self):
        """
        test login link does not present for authorized user
        """
        page = self.app.get('/', user=UserFactory())
        self.assertIn(_('login'), page)
        self.assertIn(reverse('doppler_auth_login'), page)

    def test_login_form(self):
        """
        submitting login form should result in user authorization normally
        also check validation mechanism here
        """
        raise NotImplementedError

    def test_login_view(self):
        """
        Visit login view as anonymous and fill the form to authorize.
        Higher level test comparing to previous one.
        """
        raise NotImplementedError

    def test_logout(self):
        """
        Test logout view works fine and redirects to correct url
        """
        raise NotImplementedError

#    def testLogoutAndLogin(self):
#        page = self.app.get('/', user='kmike')
#        page = page.click(_('logout')).follow()
#        assert _('logout') not in page
#        login_form = page.click(_('login'), index= 0).form
#        login_form['email'] = 'example@example.com'
#        login_form['password'] = '123'
#        result_page = login_form.submit().follow()
#        assert _('login') not in result_page
#        assert _('logout') in result_page
