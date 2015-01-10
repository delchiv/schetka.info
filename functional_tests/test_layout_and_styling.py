# coding: utf-8

from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        # Эдит зашла на домашнюю страницу
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # Она заметила, что поле ввода отцентрировано
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x']+inputbox.size['width']/2, 512, delta=5)

        # В начатом ею списке поле ввода тоже отцентировано
        inputbox.send_keys('testitem\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x']+inputbox.size['width']/2, 512, delta=5)
