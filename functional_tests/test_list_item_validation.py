import unittest
from unittest import skip

from django.test import tag
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from functional_tests.base import FunctionalTest


@tag('functional')
class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        """Тест: нельзя добавлять пустые элементы списка"""
        # Эдит открывает домашнюю страницу и случайно пытается отправить пустой элемент списка.
        # Она нажимает Enter на пустом поле ввода
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.ID, 'id_new_item').send_keys(Keys.ENTER)
        
        # Домашняя страница обновляется, и появляется сообщение об ошибке, которое говорит,
        # что элементы списка не должны быть пустыми
        self.assertEqual(
            self.wait_for(lambda x: x.find_element(By.CSS_SELECTOR, '.has-error')).text,
            "You can't have an empty list item"
        )
        # Она пробует снова, теперь с неким текстом для элемента, и теперь это срабатывает
        self.browser.find_element(By.ID, 'id_new_item').send_keys('Buy milk')
        self.browser.find_element(By.ID, 'id_new_item').send_keys(Keys.ENTER)
        # Как ни странно, Эдит решает отправить второй пустой элемент списка

        self.browser.find_element(By.ID, 'id_new_item').send_keys(Keys.ENTER)
        # Она получает аналогичное предупреждение на странице списка

        self.assertEqual(
            self.wait_for(lambda x: x.find_element(By.CSS_SELECTOR, '.has-error')).text,
            "You can't have an empty list item"
        )
        # И она может его исправить, заполнив поле неким текстом

        self.browser.find_element(By.ID, 'id_new_item').send_keys('Make tea')
        self.browser.find_element(By.ID, 'id_new_item').send_keys(Keys.ENTER)
        
        self.check_list_item_in_table('1: Buy milk')
        self.check_list_item_in_table('2: Make tea')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
