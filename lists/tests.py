from django.core.urlresolvers import resolve
from django.test import TestCase
from .views import home_page

# Create your tests here.

class TestTest(TestCase):

    def test_root_resolvers_to_home_page_view(self):
        url = resolve('/')
        self.assertEqual(url.func, home_page)