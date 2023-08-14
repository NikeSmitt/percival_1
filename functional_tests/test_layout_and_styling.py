from django.test import tag

from selenium.webdriver.common.by import By

from functional_tests.base import FunctionalTest


@tag('functional')
class LayoutAndStylingTest(FunctionalTest):
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
