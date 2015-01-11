# coding: utf-8

from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class ItemValidationTest(FunctionalTest):

    def test_cannon_add_empty_list_items(self):
        # Эдит зашла на главную страницу и случайно попыталась добавить пустой пункт.
        # Она нажала энтер на пустом поле ввода
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        # Главная страница обновилась и она увидела сообщение об ошибке
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, 'You can`t have an empty list item')

        # Она попыталась еще раз, набрав некоторый текст. Теперь добавление сработало.
        self.browser.find_element_by_id('id_new_item').send_keys('Не пустой пункт\n')
        self.check_for_row_in_list_table('1: Не пустой пункт')

        # Будучи упрямой она попыталась добавить еще один пустой пункт
        # Но получила сообщение об ошибке.
        self.browser.find_element_by_id('id_new_item').send_keys('\n')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, 'You can`t have an empty list item')
       
        # Исправила ситуацию, введя некоторый текст
        self.browser.find_element_by_id('id_new_item').send_keys('Еще не пустой пункт\n')
        self.check_for_row_in_list_table('1: Не пустой пункт')
        self.check_for_row_in_list_table('2: Еще не пустой пункт')


