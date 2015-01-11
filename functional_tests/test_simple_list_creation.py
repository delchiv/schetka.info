# coding: utf-8

from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrive_it_later(self):
        # Эдит услышала о новом хорошем онлайновом to-do листе.
        # Решила проверить его (листа) домашнюю страницу
        self.browser.get(self.server_url)

        # Она обратила внимание, что страница называется To-Do, и в заголовке написано To-Do
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Ей немедленно было предложено создать (ввсети) какое-то задание
        inputbox = self.get_item_input_box()
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
        inputbox = self.get_item_input_box()
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
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Фрэнсис создает новый список, добавляя новый пункт. У него все прозаичней...
        inputbox = self.get_item_input_box()
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

