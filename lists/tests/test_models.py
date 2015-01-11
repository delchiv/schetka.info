# coding: utf-8

from django.test import TestCase
from django.core.exceptions import ValidationError

from lists.models import Item, List

# Create your tests here.

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

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item  = Item(text='', list=list_)
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), '/lists/%s/' % (list_.id,))
