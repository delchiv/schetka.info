# coding: utf-8

from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class ItemValidationTest(FunctionalTest):

    def test_cannon_add_empty_list_items(self):
        # Эдит зашла на главную страницу и случайно попыталась добавить пустой пункт.
        # Она нажала энтер на пустом поле ввода

        # Главная страница обновилась и она увидела сообщение об ошибке

        # Она попыталась еще раз, набрав некоторый текст. Теперь добавление сработало.

        # Будучи упрямой она попыталась добавить еще один пустой пункт
        # Но получила сообщение об ошибке.
       
        # Исправила ситуацию, введя некоторый текст
        self.fail('MyError!')