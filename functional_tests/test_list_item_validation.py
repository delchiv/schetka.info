# coding: utf-8

from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class ItemValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        # Эдит зашла на главную страницу и случайно попыталась добавить пустой пункт.
        # Она нажала энтер на пустом поле ввода
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')

        # Главная страница обновилась и она увидела сообщение об ошибке
        error = self.get_error_element()
        self.assertEqual(error.text, 'You can`t have an empty list item')

        # Она попыталась еще раз, набрав некоторый текст. Теперь добавление сработало.
        self.get_item_input_box().send_keys('Не пустой пункт\n')
        self.check_for_row_in_list_table('1: Не пустой пункт')

        # Будучи упрямой она попыталась добавить еще один пустой пункт
        # Но получила сообщение об ошибке.
        self.get_item_input_box().send_keys('\n')
        error = self.get_error_element()
        self.assertEqual(error.text, 'You can`t have an empty list item')
       
        # Исправила ситуацию, введя некоторый текст
        self.get_item_input_box().send_keys('Еще не пустой пункт\n')
        self.check_for_row_in_list_table('1: Не пустой пункт')
        self.check_for_row_in_list_table('2: Еще не пустой пункт')

    def test_cannot_add_duplicate_items(self):
        # Эдит заходит на главную страницу и начинает новый список
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Buy wellies\n')
        self.check_for_row_in_list_table('1: Buy wellies')
        
        # Случайно она пытается добавить элемент повторно
        self.get_item_input_box().send_keys('Buy wellies\n')

        # И видит информативное сообщение об ошибке
        self.check_for_row_in_list_table('1: Buy wellies')
        error = self.get_error_element()
        self.assertEqual(error.text, "You've already got this in your list")


    def test_error_messages_are_cleared_on_input(self):
        # Эдит начала новый список так, что вызвала ошибку
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')
        error = self.get_error_element()
        self.assertTrue(error.is_displayed())

        # Она начала набирать текст, чтоб исправить ошибку
        self.get_item_input_box().send_keys('a')

        # Ей приятно было увидеть, что сообщение об ошибке исчезло
        error = self.get_error_element()
        self.assertFalse(error.is_displayed())
