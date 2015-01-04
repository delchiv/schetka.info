from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from .views import home_page
from .models import Item, List

# Create your tests here.

class HomePageTest(TestCase):

    def test_root_resolves_to_home_page_view(self):
        url = resolve('/')
        self.assertEqual(url.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        item = Item()
        item.text = 'First item'
        item.list = list_
        item.save()
       
        item = Item()
        item.text = 'Second item'
        item.list = list_
        item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()

        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'First item')
        self.assertEqual(first_saved_item.list, saved_list)
        self.assertEqual(second_saved_item.text, 'Second item')
        self.assertEqual(second_saved_item.list, saved_list)

class ListViewTest(TestCase):

    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='Item 1', list=list_)
        Item.objects.create(text='Item 2', list=list_)

        response = self.client.get('/lists/new-list/')

        self.assertContains(response, 'Item 1')
        self.assertContains(response, 'Item 2')

    def test_uses_list_template(self):
        response = self.client.get('/lists/new-list/')
        self.assertTemplateUsed(response, 'list.html')

class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data = {'item_text':'A new list item'}
        )

        self.assertEqual(Item.objects.count(), 1)
        item = Item.objects.first()
        self.assertEqual(item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new',
            data = {'item_text':'A new list item'}
        )

        self.assertRedirects(response, '/lists/new-list/')
