# coding: utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrive_it_later(self):
        # Эдит услышала о новом хорошем онлайновом to-do листе.
        # Решила проверить его (листа) домашнюю страницу
        self.browser.get('http://localhost:8000')

        # Она обратила внимание, что страница называется To-Do, и в заголовке написано To-Do
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Ей немедленно было предложено создать (ввсети) какое-то задание
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # Она набрала "Buy peacock feathers" в поле ввода (Хобби Эдит - приманки для рыбалки)
        inputbox.send_keys('Buy peacock feathers')

        # Когда она нажала Enter, страница обновилась. Теперь в списке значится
        # "1: Buy peacock feathers"
        inputbox.send_keys(Keys.ENTER)
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Buy peacock feathers', [row.text for row in rows])

        # На странице также осталось поле, для ввода следующего задания.
        # Эдит ввела "Use peacock feathers to make a fly" (она очень методична)
        # Страница снова обновилась и теперь отображает оба пункта
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('2: Use peacock feathers to make a fly', [row.text for row in rows])

        # Эдит стало интересно, запомнит ли сайт ее список. Затем она обратила внимание,
        # что сайт сгенерировал уникальный URL для ее списка.
        self.fail('Finish the test!')

# Она перешла по предложенной ссылке и увидела свой список

# Удовлетворенная, она пошла спать дальше :)

if __name__ == '__main__':
    unittest.main()