# coding: utf-8

from selenium import webdriver
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

        # Она обратила внимание, что страница называется To-Do
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

# Ей немедленно было предложено создать (ввсети) какое-то задание

# Она набрала "Buy peacock feathers" в поле ввода (Хобби Эдит - приманки для рыбалки)

# Когда она нажала Enter, страница обновилась. Теперь в списке значится
# "1: Buy peacock feathers"

# На странице также осталось поле, для ввода следующего задания.
# Эдит ввела "Use peacock feathers to make a fly" (она очень методична)

# Страница снова обновилась и теперь отображает оба пункта

# Эдит стало интересно, запомнит ли сайт ее список. Затем она обратила внимание,
# что сайт сгенерировал уникальный URL для ее списка.

# Она перешла по предложенной ссылке и увидела свой список

# Удовлетворенная, она пошла спать дальше :)

if __name__ == '__main__':
    unittest.main()