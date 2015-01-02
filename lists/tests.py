from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from .views import home_page

# Create your tests here.

class TestTest(TestCase):

    def test_root_resolvers_to_home_page_view(self):
        url = resolve('/')
        self.assertEqual(url.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)
