# coding: utf-8

from unittest import skip

from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape

from lists.views import home_page
from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm, EMPTY_LIST_ERROR, DUPLICATE_ITEM_ERROR

# Create your tests here.

class HomePageTest(TestCase):

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


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

    def test_can_save_a_POST_request_to_an_exixting_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%s/' % (correct_list.id,),
            data = {'text': 'Item in a correct list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        item = Item.objects.first()
        self.assertEqual(item.text, 'Item in a correct list')
        self.assertEqual(item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/%s/' % (correct_list.id,),
            data = {'text': 'Item in a correct list'}
        )

        self.assertRedirects(response, '/lists/%s/' % (correct_list.id,))

    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post('/lists/%s/' % (list_.id,), data={'text':''})

    def test_for_invalid_input_nosing_save_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)
  
    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, EMPTY_LIST_ERROR)

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%s/' % (list_.id,))
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def test_duplicate_item_validatoin_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        item = Item.objects.create(text='some text', list=list_)
        response = self.client.post('/lists/%s/' % (list_.id,), data={'text':'some text'})
        expected_error = escape(DUPLICATE_ITEM_ERROR)

        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.count(), 1)


class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data = {'text':'A new list item'}
        )

        self.assertEqual(Item.objects.count(), 1)
        item = Item.objects.first()
        self.assertEqual(item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new',
            data = {'text':'A new list item'}
        )
        list_ = List.objects.first()
        self.assertRedirects(response, '/lists/%s/' % (list_.id,))

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post(reverse('new_list'), data={'text':''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post(reverse('new_list'), data={'text':''})
        self.assertContains(response, EMPTY_LIST_ERROR)

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post(reverse('new_list'), data={'text':''})
        self.assertIsInstance(response.context['form'], ItemForm)
 
    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'text':''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

