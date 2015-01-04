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

    def test_displays_all_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='Correct item 1', list=correct_list)
        Item.objects.create(text='Correct item 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='Other item 1', list=other_list)
        Item.objects.create(text='Other item 2', list=other_list)

        response = self.client.get('/lists/%s/' % (correct_list.id,))

        self.assertContains(response, 'Correct item 1')
        self.assertContains(response, 'Correct item 2')
        self.assertNotContains(response, 'Other item 1')
        self.assertNotContains(response, 'Other item 2')

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%s/' % (list_.id,))
        self.assertTemplateUsed(response, 'list.html')

    def test_pases_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%s/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)

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
        list_ = List.objects.first()
        self.assertRedirects(response, '/lists/%s/' % (list_.id,))


class NewItemTest(TestCase):
    
    def test_can_save_a_POST_request_to_an_exixting_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%s/add_item' % (correct_list.id,),
            data = {'item_text': 'Item in a correct list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        item = Item.objects.first()
        self.assertEqual(item.text, 'Item in a correct list')
        self.assertEqual(item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/%s/add_item' % (correct_list.id,),
            data = {'item_text': 'Item in a correct list'}
        )

        self.assertRedirects(response, '/lists/%s/' % (correct_list.id,))

