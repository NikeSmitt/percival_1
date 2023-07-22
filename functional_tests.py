import unittest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
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
        assert 'To-Do' in self.browser.title
        self.fail('Закончить тест!')
        
        # Ей сразу же предлагается ввести элемент списка Она набирает в текстовом поле "Купить павлиньи перья" (ее хобби – #
        # вязание рыболовных мушек)
        
        # Когда она нажимает enter, страница обновляется, и теперь страница # содержит "1: Купить
        # павлиньи перья" в качестве элемента списка Текстовое поле по-прежнему приглашает ее добавить еще один элемент. #
        # Она вводит "Сделать мушку из павлиньих перьев" (Эдит очень методична) Страница снова обновляется,
        # и теперь показывает оба элемента ее списка Эдит интересно, запомнит ли сайт ее список. Далее она видит, что # сайт
        # сгенерировал для нее уникальный URL-адрес – об этом выводится небольшой текст с объяснениями. Она посещает этот
        # URL-адрес – ее список по-прежнему там. # Удовлетворенная, она снова ложится спать


if __name__ == '__main__':
    unittest.main(warnings='ignore')
