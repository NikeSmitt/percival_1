import time
import unittest

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

service = ChromeService(executable_path=ChromeDriverManager().install())


class NewVisitorTest(unittest.TestCase):
    
    def setUp(self) -> None:
        self.browser = webdriver.Chrome(service=service)
    
    def tearDown(self) -> None:
        self.browser.quit()
    
    def test_can_start_a_list_and_retrieve_it_later(self):
        """тест: можно начать список покупок и получить его позже"""
        
        # Эдит слышала про крутое новое онлайн-приложение со списком
        self.browser.get('http://localhost:8000')
        
        # Она видит, что заголовок и шапка страницы говорят о списках # неотложных дел
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)
        
        # Ей сразу же предлагается ввести элемент списка
        
        input_box = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        # Она набирает в текстовом поле "Купить павлиньи перья" (ее
        # хобби – # вязание рыболовных мушек)
        input_box.send_keys('Купить павлиньи перья')
        # Когда она нажимает enter, страница обновляется, и теперь страница # содержит "1: Купить павлиньи перья" в
        # качестве элемента списка
        
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)
        
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn('1: Купить павлиньи перья', [row.text for row in rows])
        
        # Текстовое поле по-прежнему приглашает ее добавить еще один элемент.
        input_box = self.browser.find_element(By.ID, 'id_new_item')
        
        # Она вводит "Сделать мушку из павлиньих перьев" (Эдит очень методична)
        input_box.send_keys('Сделать мушку из павлиньих перьев')
        
        # Страница снова обновляется, и теперь показывает
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)
        
        # оба элемента ее списка Эдит интересно, запомнит ли сайт ее список.
        
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn('1: Купить павлиньи перья', [row.text for row in rows])
        self.assertIn('2: Сделать мушку из павлиньих перьев', [row.text for row in rows])
        
        # Далее она видит, что сайт сгенерировал для нее уникальный URL-адрес – об этом выводится небольшой текст с объяснениями. Она посещает этот
        # URL-адрес – ее список по-прежнему там. # Удовлетворенная, она снова ложится спать
        
        self.fail('Закончить тест!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
