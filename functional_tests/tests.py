# coding: utf-8
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrive_it_later(self):
        # Эдит услышала о новом хорошем онлайновом to-do листе.
        # Решила проверить его (листа) домашнюю страницу
        self.browser.get(self.live_server_url)

        # Она обратила внимание, что страница называется To-Do, и в заголовке написано To-Do
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Ей немедленно было предложено создать (ввсети) какое-то задание
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # Она набрала "Buy peacock feathers" в поле ввода (Хобби Эдит - приманки для рыбалки)
        inputbox.send_keys('Buy peacock feathers')

        # Когда она нажала Enter, страница обновилась (новый url). 
        # Теперь в списке значится "1: Buy peacock feathers"
        inputbox.send_keys(Keys.ENTER)
        edith_url = self.browser.current_url
        self.assertRegex(edith_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # На странице также осталось поле, для ввода следующего задания.
        # Эдит ввела "Use peacock feathers to make a fly" (она очень методична)
        # Страница снова обновилась и теперь отображает оба пункта
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # Новый пользователь Фрэнсис зашел на сайт
         
        ## Используем новую сессию браузера, чтоб убедиться, что данные прошлого пользователя не сохранены
        self.browser.refresh()
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Фрэнсис заходит на главную. Там нет информации, принадлежащей Эдит
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Фрэнсис создает новый список, добавляя новый пункт. У него все прозаичней...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # Фрэнсис получает свой собственный уникальный url
        francis_url = self.browser.current_url
        self.assertRegex(francis_url, '/lists/.+')
        self.assertNotEqual(francis_url, edith_url)

        # И снова, тут нет никакой связи со списком Эдит
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

    def test_layout_and_styling(self):
        # Эдит зашла на домашнюю страницу
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # Она заметила, что поле ввода отцентрировано
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x']+inputbox.size['width']/2, 512, delta=5)

        # В начатом ею списке поле ввода тоже отцентировано
        inputbox.send_keys('testitem\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x']+inputbox.size['width']/2, 512, delta=5)

 
