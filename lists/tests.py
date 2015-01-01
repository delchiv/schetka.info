from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from .views import home_page

# Create your tests here.

class TestTest(TestCase):

    def test_root_resolvers_to_home_page_view(self):
        url = resolve('/')
        self.assertEqual(url.func, home_page)

    def test_home_page_returns_valid_html(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>To-Do lists</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))
