import time
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import tag

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


@tag('functional')
class NewVisitorTest(StaticLiveServerTestCase):
    """New visitor tests"""
    
    def setUp(self) -> None:
        self.browser = NewVisitorTest.get_new_browser()
    
    def tearDown(self) -> None:
        self.browser.quit()
    
    @staticmethod
    def get_new_browser():
        service = ChromeService(executable_path=ChromeDriverManager(version='114.0.5735.90').install())
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        return webdriver.Chrome(service=service, options=options)
    
    def check_list_item_in_table(self, item_text):
        # table = self.browser.find_element(By.ID, 'id_list_table')
        table = WebDriverWait(self.browser, timeout=5).until(lambda x: x.find_element(By.ID, 'id_list_table'))
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(item_text, [row.text for row in rows])
    
    def test_can_start_a_list_for_one_user(self):
        """Тест: начать список для одного пользователя"""
        
        # Эдит слышала про крутое новое онлайн-приложение со списком
        self.browser.get(self.live_server_url)
        
        # Она видит, что заголовок и шапка страницы говорят о списках # неотложных дел
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('список неотложных дел', header_text)
        
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
        
        self.check_list_item_in_table('1: Купить павлиньи перья')
        
        # Текстовое поле по-прежнему приглашает ее добавить еще один элемент.
        input_box = self.browser.find_element(By.ID, 'id_new_item')
        
        # Она вводит "Сделать мушку из павлиньих перьев" (Эдит очень методична)
        input_box.send_keys('Сделать мушку из павлиньих перьев')
        input_box.send_keys(Keys.ENTER)
        
        # Страница снова обновляется, и теперь показывает
        # оба элемента ее списка Эдит интересно, запомнит ли сайт ее список.
        
        self.check_list_item_in_table('1: Купить павлиньи перья')
        self.check_list_item_in_table('2: Сделать мушку из павлиньих перьев')
        
        # Далее она видит, что сайт сгенерировал для нее уникальный URL-адрес – об этом выводится
        # небольшой текст с объяснениями. Она посещает этот URL-адрес – ее список по-прежнему там.
        # Удовлетворенная, она снова ложится спать
    
    def test_multiple_users_can_start_lists_at_different_urls(self):
        """Тест: многочисленные пользователи могут начать списки по разным url"""
        # Эдит начинает новый список
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element(By.ID, 'id_new_item')
        input_box.send_keys('Купить павлиньи перья')
        input_box.send_keys(Keys.ENTER)
        self.check_list_item_in_table('1: Купить павлиньи перья')
        
        # Она замечает, что ее список имеет уникальный URL-адрес
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        
        # Теперь новый пользователь, Валера, приходит на сайт.
        # Мы используем новый сеанс браузера, тем самым обеспечивая,
        # чтобы никакая ## информация от Эдит не прошла через данные cookie и пр.
        
        self.browser.quit()
        self.browser = NewVisitorTest.get_new_browser()
        
        # Валера посещает домашнюю страницу. Нет никаких признаков списка Эдит
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertNotIn('Сделать мушку', page_text)
        
        # Валера начинает новый список, вводя новый элемент
        
        input_box = self.browser.find_element(By.ID, 'id_new_item')
        input_box.send_keys('Купить молоко')
        input_box.send_keys(Keys.ENTER)
        self.check_list_item_in_table('1: Купить молоко')
        
        # Валера получает уникальный адрес
        valera_list_url = self.browser.current_url
        self.assertRegex(valera_list_url, '/lists/.+')
        self.assertNotEqual(valera_list_url, edith_list_url)
        
        # Нет следа от списка Эдит
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertIn('Купить молоко', page_text)
    
    def test_layout_and_styling(self):
        """Тест макета и стилевого оформления"""
        # Эдит открывает домашнюю страницу
        
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        
        # Она замечает, что поле ввода аккуратно центрировано
        input_box = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=10  # delta for 10 px
        )
        


if __name__ == '__main__':
    unittest.main(warnings='ignore')
