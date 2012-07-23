"""
Studio: Doppler
Author: Grigoriy Beziuk
Project: Django Application Skeleton
Module: Basic user authorization
Part: Tests
"""
from django.core.urlresolvers import reverse
from django_webtest import WebTest
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
import factory
from .forms import LoginForm

class UserFactory(factory.Factory):
    """
    User model factory
    """
    FACTORY_FOR = User
    username = 'sample_user'
    is_active = True

class AuthAcceptanceTest(WebTest):
    """
    Acceptance test for login and logout functionality
    """
    
    def _get_page(self, url='/', **kwargs):
        """
        This method is used in case of site root page is redirecting to another inner page
        """
        page = self.app.get(url, **kwargs)
        if page.status == '302 FOUND':
            page = page.follow()
        return page

    def setUp(self):
        """
        Initialization
        """
        self.test_password = 'password'
        self.test_wrong_password = 'wrong_password'
        self.test_username = 'username'
        self.user = UserFactory(username=self.test_username)
        self.user.set_password(self.test_password)
        self.user.save()

    def test_login_link_present_for_anonymous_user(self):
        """
        test login link present for anonymous user
        """
        page = self._get_page()
        self.assertIn(_('login'), page)
        self.assertIn(reverse('auth_login'), page)

    def test_logout_link_does_not_present_for_anonymous_user(self):
        """
        test logout link does not present for anonymous user
        """
        page = self._get_page()
        self.assertNotIn(_('Logout'), page)
        self.assertNotIn(reverse('auth_logout'), page)

    def test_logout_link_present_for_authorized_user(self):
        """
        test logout link present for authorized user
        """
        page = self._get_page('/', user=UserFactory())
        self.assertIn(_('Logout'), page)
        self.assertIn(reverse('auth_logout'), page)

    def test_login_link_does_not_present_for_authorized_user(self):
        """
        test login link does not present for authorized user
        """
        page = self._get_page('/', user=UserFactory())
        self.assertNotIn(_('login'), page)
        self.assertNotIn(reverse('auth_login'), page)

    def test_login_form_validation(self):
        """
        checking login form validation mechanism here
        """
        self.assertFalse(LoginForm().is_valid())
        self.assertFalse(LoginForm(data={'username': self.test_username}).is_valid())
        self.assertFalse(LoginForm(data={'password': self.test_password}).is_valid())
        self.assertTrue(LoginForm(data={'username': self.test_username ,'password': self.test_password}).is_valid())

    def test_login_view(self):
        """
        Visit login view as anonymous and fill the form to authorize.
        Higher level test comparing to previous one.
        """
        page = self._get_page(reverse('auth_login'))
        self.assertTrue(page.context['user'].is_anonymous())
        self.assertIn(LoginForm.html_id, page.forms)
        login_form = page.forms[LoginForm.html_id]
        login_form['username'] = self.test_username
        login_form['password'] = self.test_password
        sumbit_result = login_form.submit().follow()
        if sumbit_result.status == '302 FOUND':
            sumbit_result = sumbit_result.follow()
        self.assertFalse(sumbit_result.context['user'].is_anonymous())
        self.assertEqual(sumbit_result.context['user'].pk, self.user.pk)

    def test_logout(self):
        """
        Test logout view works fine and redirects to correct url
        """
        page = self._get_page(reverse('auth_logout'), user=self.user) #why don't I need add a 'follow()' here?
        self.assertTrue(page.context['user'].is_anonymous())